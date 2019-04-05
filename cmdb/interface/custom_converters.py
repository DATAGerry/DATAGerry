import logging
from werkzeug.routing import BaseConverter

LOGGER = logging.getLogger(__name__)


class DictConverter(BaseConverter):

    def to_python(self, value):
        """TODO Implement to dict convert"""
        return value.split('+')

    def to_url(self, values):
        return '+'.join(BaseConverter.to_url(value)
                        for value in values)
