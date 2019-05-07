# dataGerry - OpenSource Enterprise CMDB
# Copyright (C) 2019 NETHINKS GmbH
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
Event Management
Module for sending/receiving events between CMDB processes
"""
import logging
import queue
import multiprocessing
import threading
import pika
from cmdb.event_management.event import Event
from cmdb.utils.system_reader import SystemConfigReader

LOGGER = logging.getLogger(__name__)


class EventManager:
    """
    Abstract class for event handling
    """

    def __init__(self, receiver_callback):
        """
        EventManager init
        Args:
            receiver_callback: function, that is called if events were
                received
        """
        self._receiver_callback = receiver_callback

    def send_event(self, event):
        """sends an  event

        Args:
            event: the created event to send

        """
        pass

    def get_send_queue(self):
        """get the queue for sending events

        Events can be put into a queue, the EventManager will receive
        events from that queue and send them to the other daemons. This
        function will return a reference to the send queue

        Returns:
            A reference to the queue
        """
        pass

    def shutdown(self):
        """shutdown the EventManager"""
        pass


class EventManagerAmqp(EventManager):
    """EventManager using a message broker and the AMQP protocol

    This EventManager implementation uses the AMQP procotol to connect
    to a message broker. It was developed and tested with RabbitMQ.
    It starts an EventSender and an EventReceiver thread.
    """

    def __init__(self, flag_shutdown, receiver_callback, process_id=None, event_types=["#"], flag_multiproc=False):
        """Creates an instance of EventManagerAmqp

        Args:
            flag_shutdown(threading.Event): flag for handling shutdown
            receiver_callback(func): callback function for processing
                received events
            process_id(str): process identifier (process name)
            event_types(list): list of event types, that will be processed
            flag_multiproc(bool): switch, if EventManager should be used
                by multiple processes
        """
        super(EventManagerAmqp, self).__init__(receiver_callback)

        # store variables
        self.__process_id = process_id
        self.__event_types = event_types
        self.__multiprocessing = flag_multiproc

        # create queue for events to send
        if self.__multiprocessing:
            self.__queue_send = multiprocessing.Queue()
        else:
            self.__queue_send = queue.Queue()

        # setup shutdown flag
        self.__flag_shutdown = flag_shutdown

        # create producer thread
        self.__producer = EventSenderAmqp(self.__queue_send, self.__flag_shutdown, self.__process_id)
        self.__producer.start()

        # create consumer thread
        self.__consumer = EventReceiverAmqp(self._receiver_callback, self.__flag_shutdown,
                                            self.__process_id, self.__event_types)
        self.__consumer.start()

    def send_event(self, event):
        self.__queue_send.put(event)

    def get_send_queue(self):
        return self.__queue_send

    def shutdown(self):
        # set shutdown flag
        self.__flag_shutdown.set()
        # wait for producer and consumer to end
        self.__producer.join()
        self.__consumer.join()


class EventSenderAmqp(threading.Thread):
    """EventSender part of the EventManagerAmqp

    This part of the EventManagerAmqp is responsible for sending events
    to the message broker using the protocol AMQP.
    """

    def __init__(self, message_queue, flag_shutdown, process_id=None):
        """Creates an instance of EventSenderAmqp

        Args:
            message_queue(queue.Queue): handler of a queue for sending events
            flag_shutdown(threading.Event): flag for handling shutdown
            process_id(str): process identifier (process name)
        """
        super(EventSenderAmqp, self).__init__()
        self.__queue = message_queue
        self.__flag_shutdown = flag_shutdown
        self.__process_id = process_id

        # get configuration
        self.__config_mq = SystemConfigReader().get_all_values_from_section('MessageQueueing')
        self.__config_host = self.__config_mq.get("host", "127.0.0.1")
        self.__config_port = self.__config_mq.get("port", "5672")
        self.__config_username = self.__config_mq.get("username", "guest")
        self.__config_password = self.__config_mq.get("password", "guest")
        self.__config_exchange = self.__config_mq.get("exchange", "netcmdb.eventbus")
        self.__config_retries = int(self.__config_mq.get("connection_attempts", "5"))
        self.__config_retrydelay = int(self.__config_mq.get("retry_delay", "6"))
        self.__config_tls = False
        if self.__config_mq.get("use_tls", "False") in ("true", "True", "1", "yes"):
            self.__config_tls = True

        # define variables
        self.__connection = None
        self.__channel = None

    def __init_connection(self):
        """create a connection to message broker"""
        try:
            credentials = pika.credentials.PlainCredentials(self.__config_username, self.__config_password)
            self.__connection = pika.BlockingConnection(pika.ConnectionParameters(
                host=self.__config_host,
                port=self.__config_port,
                connection_attempts=self.__config_retries,
                retry_delay=self.__config_retrydelay,
                credentials=credentials,
                ssl=self.__config_tls
            ))
            self.__channel = self.__connection.channel()
            self.__channel.exchange_declare(
                exchange=self.__config_exchange,
                exchange_type="topic"
            )
        except pika.exceptions.AMQPConnectionError:
            LOGGER.error("{}: EventSenderAmqp connection error".format(self.__process_id))
            self.__flag_shutdown.set()

    def run(self):
        """run the event sender"""
        # init connection to broker
        self.__init_connection()

        # check queue for new events
        while not self.__flag_shutdown.is_set():
            try:
                try:
                    event = self.__queue.get(block=True, timeout=2)
                    event_type = event.get_type()
                    event_serialized = event.json_repr()
                    self.__channel.basic_publish(exchange=self.__config_exchange,
                                                 routing_key=event_type,
                                                 body=event_serialized)
                except queue.Empty:
                    self.__connection.process_data_events()
            # handle AMQP connection errors
            except pika.exceptions.AMQPConnectionError:
                LOGGER.warning("connection to broker lost, try to reconnect...")
                self.__init_connection()


class EventReceiverAmqp(threading.Thread):
    """EventReceiver part of the EventManagerAmqp

    This part of the EventManagerAmqp is responsible for receiving events
    from the message broker using the protocol AMQP. Only configured event
    types were processed (e.g. cmdb.core.objects.added)
    """

    def __init__(self, receiver_callback, flag_shutdown, process_id=None, event_types=["#"]):
        """Creates an instance of EventReceiverAmqp

        Args:
            receiver_callback(func): callback function for processing
                received events
            flag_shutdown(threading.Event): flag for handling shutdown
            process_id(str): process identifier (process name)
            event_types(list): list of event types, that will be processed
        """
        super(EventReceiverAmqp, self).__init__()
        self.__receiver_callback = receiver_callback
        self.__flag_shutdown = flag_shutdown
        self.__process_id = process_id
        self.__event_types = event_types

        # get configuration
        self.__config_mq = SystemConfigReader().get_all_values_from_section('MessageQueueing')
        self.__config_host = self.__config_mq.get("host", "127.0.0.1")
        self.__config_port = self.__config_mq.get("port", "5672")
        self.__config_username = self.__config_mq.get("username", "guest")
        self.__config_password = self.__config_mq.get("password", "guest")
        self.__config_exchange = self.__config_mq.get("exchange", "netcmdb.eventbus")
        self.__config_retries = int(self.__config_mq.get("connection_attempts", "5"))
        self.__config_retrydelay = int(self.__config_mq.get("retry_delay", "6"))
        self.__config_tls = False
        if self.__config_mq.get("use_tls", "False") in ("true", "True", "1", "yes"):
            self.__config_tls = True

        # define variables
        self.__connection = None
        self.__channel = None

    def __process_event_cb(self, ch, method, properties, body):
        """event processing

        this callback function is executed, if an event was reveived.

        Args:
            ch: AMQP channel
            method: AMQP method
            properties: AMQP properties
            body: AMQP message body
        """
        event = Event.create_event(body)
        # allow None values, if event receiving should be ignored
        if self.__receiver_callback:
            self.__receiver_callback(event)

    def __check_shutdown_flag(self):
        """check, if the shutdown flag was set"""
        # reinstall shutdown check
        self.__connection.add_timeout(2, self.__check_shutdown_flag)
        # check shutdown flag
        if self.__flag_shutdown.is_set():
            self.__channel.stop_consuming()
            self.__connection.close()

    def __init_connection(self):
        """create a connection to message broker"""
        try:
            # init connection to broker
            credentials = pika.credentials.PlainCredentials(self.__config_username, self.__config_password)
            self.__connection = pika.BlockingConnection(pika.ConnectionParameters(
                host=self.__config_host,
                port=self.__config_port,
                connection_attempts=self.__config_retries,
                retry_delay=self.__config_retrydelay,
                credentials=credentials,
                ssl=self.__config_tls
            ))
            self.__channel = self.__connection.channel()
            self.__channel.exchange_declare(exchange=self.__config_exchange, exchange_type="topic")
            queue_name = ""
            if self.__process_id:
                queue_name = "{}.{}".format(self.__config_exchange, self.__process_id)
            queue_declare_result = self.__channel.queue_declare(queue=queue_name, exclusive=True)
            queue_handler = queue_declare_result.method.queue
            for event_type in self.__event_types:
                self.__channel.queue_bind(exchange=self.__config_exchange, queue=queue_handler, routing_key=event_type)

            # register callback function for event handling
            self.__channel.basic_consume(self.__process_event_cb, queue=queue_handler, no_ack=True)
        except pika.exceptions.AMQPConnectionError:
            LOGGER.error("{}: EventReceiverAmqp connection error".format(self.__process_id))
            self.__flag_shutdown.set()

    def run(self):
        """run the event receiver"""
        # init connection to broker
        self.__init_connection()
        while not self.__flag_shutdown.is_set():
            try:
                # start handling events
                self.__connection.add_timeout(2, self.__check_shutdown_flag)
                self.__channel.start_consuming()
            # handle AMQP connection errors
            except pika.exceptions.AMQPConnectionError:
                LOGGER.warning("connection to broker lost, try to reconnect...")
                self.__init_connection()
