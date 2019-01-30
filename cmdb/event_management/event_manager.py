import json
import queue
import multiprocessing
import threading
import pika
from cmdb.event_management.event import Event
from cmdb.utils import get_system_config_reader

class EventManager:

    def __init__(self, receiver_callback):
        pass

    def send_event(self, event):
        pass

    def get_send_queue(self):
        pass

    def shutdown():
        pass


class EventManagerAmqp(EventManager):

    def __init__(self, flag_shutdown, receiver_callback, process_id=None, event_types=["#"], flag_multiproc=False):
        # store variables
        self.__process_id = process_id
        self.__receiver_callback = receiver_callback
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
        self.__consumer = EventReceiverAmqp(self.__receiver_callback, self.__flag_shutdown, self.__process_id, self.__event_types)
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

    def __init__(self, queue, flag_shutdown, process_id=None):
        super(EventSenderAmqp, self).__init__()
        self.__queue = queue
        self.__flag_shutdown = flag_shutdown
        self.__process_id = process_id

        # get configuration
        self.__config_mq = get_system_config_reader().get_all_values_from_section('MessageQueueing')
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


    def __init_connection(self):
        # init connection to broker
        try:
            credentials = pika.credentials.PlainCredentials(self.__config_username, self.__config_password)
            self.__connection = pika.BlockingConnection(pika.ConnectionParameters(
                                                            host=self.__config_host,
                                                            port=self.__config_port,
                                                            connection_attempts=self.__config_retries, 
                                                            retry_delay=self.__config_retrydelay,
                                                            credentials=credentials,
                                                            ssl=self.__config_tls
                                                            )
                                                        )
            self.__channel = self.__connection.channel()
            self.__channel.exchange_declare(
                exchange=self.__config_exchange,
                exchange_type="topic"
            )
        except pika.exceptions.AMQPConnectionError:
            print("{}: EventSenderAmqp connection error".format(self.__process_id))
            self.__flag_shutdown.set()

    def run(self):
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
                print("connection to broker lost, try to reconnect...")
                self.__init_connection()


class EventReceiverAmqp(threading.Thread):

    def __init__(self, receiver_callback, flag_shutdown, process_id=None, event_types=["#"]):
        super(EventReceiverAmqp, self).__init__()
        self.__receiver_callback = receiver_callback
        self.__flag_shutdown = flag_shutdown
        self.__process_id = process_id
        self.__event_types = event_types

        # get configuration
        self.__config_mq = get_system_config_reader().get_all_values_from_section('MessageQueueing')
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

    def __process_event_cb(self, ch, method, properties, body):
        event = Event.create_event(body)
        # allow None values, if event receiving should be ignored
        if self.__receiver_callback:
            self.__receiver_callback(event)

    def __check_shutdown_flag(self):
        # reinstall shutdown check
        self.__connection.add_timeout(2, self.__check_shutdown_flag)
        # check shutdown flag
        if self.__flag_shutdown.is_set():
            self.__channel.stop_consuming()
            self.__connection.close()

    def __init_connection(self):
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
                                                            )
                                                        )
            self.__channel = self.__connection.channel()
            self.__channel.exchange_declare(exchange=self.__config_exchange, exchange_type="topic")
            queue_name = ""
            if self.__process_id:
                queue_name = "{}.{}".format(self.__config_exchange, self.__process_id)
            queue_declare_result = self.__channel.queue_declare(queue=queue_name, exclusive=True)
            queue = queue_declare_result.method.queue
            for event_type in self.__event_types:
                self.__channel.queue_bind(exchange=self.__config_exchange, queue=queue, routing_key=event_type)

            # register callback function for event handling
            self.__channel.basic_consume(self.__process_event_cb, queue=queue, no_ack=True)
        except pika.exceptions.AMQPConnectionError:
            print("{}: EventReceiverAmqp connection error".format(self.__process_id))
            self.__flag_shutdown.set()


    def run(self):
        # init connection to broker
        self.__init_connection()
        while not self.__flag_shutdown.is_set():
            try:
                # start handling events
                self.__connection.add_timeout(2, self.__check_shutdown_flag)
                self.__channel.start_consuming()
            # handle AMQP connection errors
            except pika.exceptions.AMQPConnectionError:
                print("connection to broker lost, try to reconnect...")
                self.__init_connection()
