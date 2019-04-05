import logging
from werkzeug.routing import BaseConverter

LOGGER = logging.getLogger(__name__)


class DictConverter(BaseConverter):

    def to_python(self, value):
        """TODO Implement to dict convert"""
        return value.split('+')

