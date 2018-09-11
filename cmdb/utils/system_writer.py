"""
Writer module for database based system configurations
"""
from cmdb.data_storage.database_manager import DatabaseManagerMongo
from cmdb.data_storage.database_manager import NoDocumentFound


class SystemWriter:
    """

    """

    def __init__(self, writer: DatabaseManagerMongo):
        """

        Args:
            writer:
        """
        self.writer = writer

    def write(self, _id: str, data: dict) -> str:
        """

        Args:
            _id:
            data:

        Returns:

        """
        raise NotImplementedError

    def update(self, _id: str or int, data: dict) -> str:
        """

        Args:
            _id:
            data:

        Returns:

        """
        raise NotImplementedError

    def verify(self, _id: int, data: dict) -> bool:
        """

        Returns:

        """
        raise NotImplementedError


class SystemSettingsWriter(SystemWriter):
    """

    """
    COLLECTION = 'settings.conf'

    def __init__(self, database_manager: DatabaseManagerMongo):
        """

        Args:
            database_manager:
        """
        super(SystemSettingsWriter, self).__init__(database_manager)

    def write(self, _id: str, data: dict):
        """
        TODO: Setup bug fixen
        Args:
            _id:
            data:

        Returns:

        """
        try:
            writing_document = self.writer.find_one_by(collection=self.COLLECTION, filter={'_id': _id})
        except NoDocumentFound:
            new_id = self.writer.insert(collection=self.COLLECTION, data={'_id': _id})
            writing_document = self.writer.find_one_by(collection=self.COLLECTION, filter={'_id': new_id})

        writing_document.update(data)
        ack = self.writer.update_with_internal(
            collection=self.COLLECTION,
            _id=writing_document['_id'],
            data=writing_document
        )
        return ack

    def update(self, _id: str or int, data: dict) -> str:
        """

        Args:
            _id:
            data:

        Returns:

        """
        from cmdb.data_storage.database_utils import convert_form_data
        new_data = convert_form_data(data)
        current_setting = self.writer.find_one_by(collection=self.COLLECTION, filter={'_id': _id})
        current_setting.update(new_data)
        ack = self.writer.update_with_internal(collection=self.COLLECTION, _id=_id, data=current_setting)
        return ack

    def verify(self, _id: str, data: dict) -> bool:
        """

        Args:
            _id:
            data:

        Returns:

        """
        verify_document = self.writer.find_one_by(collection=self.COLLECTION, filter={'_id': _id})
        if verify_document != data:
            return False
        return True


class NoEntryFoundError(Exception):

    def __init__(self, _id):
        super().__init__()
        self.message = "Entry with the id {} was not found".format(_id)
