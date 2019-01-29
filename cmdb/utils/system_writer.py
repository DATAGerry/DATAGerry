"""
Configuration module for settings in file format and in the database
"""
from cmdb.data_storage.database_manager import DatabaseManagerMongo
from cmdb.data_storage.database_manager import NoDocumentFound
from cmdb.utils.error import CMDBError


class SystemWriter:
    """
    Superclass for general write permissions
    Watch out with the collection constants. In Mongo the Settings Collection is pre-defined
    """

    COLLECTION = 'settings.*'

    def __init__(self, writer: DatabaseManagerMongo):
        """
        Default constructor
        Args:
            writer: Database manager instance
        """
        self.writer = writer

    def write(self, _id: str, data: dict) -> str:
        """
        write data into database
        it' the only module where no public_id is used
        Args:
            _id: database entry identifier
            data: data to write

        Returns:
            acknowledgment: based on database manager
        """
        raise NotImplementedError

    def update(self, _id: str or int, data: dict) -> str:
        """
        update entry in database
        Args:
            _id: database entry identifier
            data: data to update

        Returns:
            acknowledgment: based on database manager
        """
        raise NotImplementedError

    def verify(self, _id: int, data: dict) -> bool:
        """
        Checks if configuration entry exists
        Returns: True if exists - else False

        """
        raise NotImplementedError


class SystemSettingsWriter(SystemWriter):
    """

    """
    COLLECTION = 'settings.conf'

    def __init__(self, database_manager: DatabaseManagerMongo):
        """
        Init database writer with DatabaseManagerMongo
        Args:
            database_manager: Database connection
        """
        super(SystemSettingsWriter, self).__init__(database_manager)

    def write(self, _id: str, data: dict) -> str:
        """
        Write new settings in database
        Args:
            _id: new settings_id
            data: data to write
        Returns:
            acknowledgment: based on database manager
        TODO: auto find _id

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
        Update existing setting in database
        Args:
            _id: settings entry id
            data: data to update

        Returns:
            acknowledgment: based on database manager

        TODO: Error handling
        """
        from cmdb.data_storage.database_utils import convert_form_data
        new_data = convert_form_data(data)
        current_setting = self.writer.find_one_by(collection=self.COLLECTION, filter={'_id': _id})
        current_setting.update(new_data)
        ack = self.writer.update_with_internal(collection=self.COLLECTION, _id=_id, data=current_setting)
        return ack

    def verify(self, _id: str, data: dict = None) -> bool:
        """
        Checks if setting exists and has data
        Args:
            _id: settings entry id
            data: verify if has same data

        Returns:
            bool if entry exists and has data (compare), otherwise false
        """
        try:
            verify_document = self.writer.find_one_by(collection=self.COLLECTION, filter={'_id': _id})
        except (NoEntryFoundError, CMDBError):
            return False

        if verify_document != data and data is not None:
            return False
        return True


class NoEntryFoundError(CMDBError):
    """
    Error if no entry exists
    """

    def __init__(self, _id):
        super().__init__()
        self.message = "Entry with the id {} was not found".format(_id)
