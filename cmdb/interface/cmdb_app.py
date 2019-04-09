from flask import Flask
import logging

LOGGER = logging.getLogger(__name__)


class BaseCmdbApp(Flask):

    def __init__(self, import_name: str):
        super(BaseCmdbApp, self).__init__(import_name)
