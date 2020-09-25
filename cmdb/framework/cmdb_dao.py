# DATAGERRY - OpenSource Enterprise CMDB
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

import logging

try:
    from cmdb.utils.error import CMDBError
except ImportError:
    CMDBError = Exception

LOGGER = logging.getLogger(__name__)


class CmdbDAO:
    """The data access object is the basic presentation if objects and
    their necessary dependent classes are to be stored in the database.

    Attributes;
        DAO_ASCENDING (int): dao sort order ascending
        DAO_DESCENDING (int): dao sort order descending
        COLLECTION (str): name of the database table - should always be overwritten
        IGNORED_INIT_KEYS (list, optional): list of default init keys which an specific object won't need
        REQUIRED_INIT_KEYS (list, optional): list of default parameters which an object needs to work
        VERSIONING_MAJOR (int): addend for major version updates
        VERSIONING_MINOR (int): addend for minor version updates
        VERSIONING_PATCH (int): addend for small patches

    Note:
        COLLECTION and REQUIRED_INIT_KEYS should always be overwritten by inherited classes!!!
    """

    DAO_ASCENDING = 1
    DAO_DESCENDING = -1
    COLLECTION = 'framework.*'
    __SUPER_INIT_KEYS = [
        'public_id'
    ]
    __SUPER_INDEX_KEYS = [
        {'keys': [('public_id', DAO_ASCENDING)], 'name': 'public_id', 'unique': True}
    ]
    IGNORED_INIT_KEYS = []
    REQUIRED_INIT_KEYS = []
    INDEX_KEYS = []
    VERSIONING_MAJOR = 2
    VERSIONING_MINOR = 1
    VERSIONING_PATCH = 0

    def __init__(self, public_id, **kwargs):
        """
        All parameters inside *kwargs will be auto convert to attributes
        Args:
            **kwargs: list of parameters
        """
        self.public_id: int = int(public_id)
        for key in kwargs:
            setattr(self, key, kwargs[key])

    def get_public_id(self) -> int:
        """
        get the public id of current element

        Note:
            Since the dao object is not initializable
            the child class object will inherit this function
            SHOULD NOT BE OVERWRITTEN!

        Returns:
            int: public id

        Raises:
            NoPublicIDError: if `public_id` is zero or not set

        """
        if self.public_id == 0 or self.public_id is None:
            raise NoPublicIDError()
        return self.public_id

    def has_object_id(self) -> bool:
        """
        checks if object already has a database _id

        Note:
            Notice! Database _id is not the same as the public_id

        Returns:
            True if attribute is set, False otherwise.
        """
        if hasattr(self, '_id'):
            return True
        return False

    def __new__(cls, *args, **kwargs):
        """
        auto call function by object initialization
        checks if all required keys for cmdb usage are present
        @deprecated_implementation
        if not all(key in key_list for key in cls.REQUIRED_INIT_KEYS):
        raise InitKeyNotFoundError()

        Returns:
            Instance of the object

        Raises:
            RequiredInitKeyNotFoundError: if some given attributes are not inside the requirement lists


        """
        init_keys = cls.__SUPER_INIT_KEYS + cls.REQUIRED_INIT_KEYS
        if len(cls.IGNORED_INIT_KEYS) > 0:
            init_keys = [i for j, i in enumerate(init_keys) if j in cls.IGNORED_INIT_KEYS]
        for req_key in init_keys:
            if req_key in kwargs:
                continue
            else:
                raise RequiredInitKeyNotFoundError(req_key)
        return super(CmdbDAO, cls).__new__(cls)

    @classmethod
    def get_index_keys(cls):
        from pymongo import IndexModel
        index_list = list()
        for index in cls.INDEX_KEYS + cls.__SUPER_INDEX_KEYS:
            index_list.append(IndexModel(**index))
        return index_list

    @classmethod
    def from_data(cls, data: dict) -> "CmdbDAO":
        raise NotImplementedError()

    @classmethod
    def to_json(cls, instance: "CmdbDAO") -> dict:
        raise NotImplementedError()

    def update_version(self, update) -> str:
        """
        Update the version number of the object

        Args:
            update (int): update step

        Returns:
            new version number

        Raises:
            NoVersionError: if object has no version control
            TypeError: if version is not a float
        """
        if not hasattr(self, 'version') or self.version is None:
            raise NoVersionError(self.get_public_id())
        updater_version = _Versioning(
            *map(int, self.version.split('.'))
        )

        if type(updater_version) is not _Versioning:
            raise TypeError('Version type must be a _Versioning')

        if update == self.VERSIONING_MAJOR:
            updater_version.update_major()
        elif update == self.VERSIONING_MINOR:
            updater_version.update_minor()
        else:
            updater_version.update_patch()
        self.version = updater_version.__repr__()
        return self.version

    def get_version(self) -> str:
        """
        Get version number if exists
        Returns:
            version number
        """
        if self.version:
            return self.version
        else:
            raise NoVersionError(self.get_public_id())

    def to_database(self) -> dict:
        """
        quick and dirty database converter
        at the moment it only returns the dict, but anyway should be used.
        Returns:
            dict: attribute dict of object
        """
        return self.__dict__

    def __repr__(self):
        from cmdb.utils.helpers import debug_print
        return debug_print(self)


class _Versioning:
    """
    Helper class for object/type versioning
    """

    def __init__(self, major: int = 1, minor: int = 0, patch: int = 0):
        """
        Args:
            major: core changes with no compatibility
            minor: code changes
            patch: little fixes
        """
        self.major = major
        self.minor = minor
        self.patch = patch

    @property
    def major(self):
        return self._major

    @major.setter
    def major(self, value):
        if type(value) is not int:
            raise VersionTypeError('major', str(value))
        self._major = value

    def update_major(self) -> int:
        self.major += 1
        return self.major

    @property
    def minor(self):
        return self._minor

    @minor.setter
    def minor(self, value):
        if type(value) is not int:
            raise VersionTypeError('major', str(value))
        self._minor = value

    def update_minor(self) -> int:
        self.minor += 1
        return self.minor

    @property
    def patch(self):
        return self._patch

    @patch.setter
    def patch(self, value):
        if type(value) is not int:
            raise VersionTypeError('major', str(value))
        self._patch = value

    def update_patch(self) -> int:
        self.patch += 1
        return self.patch

    def __repr__(self):
        return '{}.{}.{}'.format(self.major, self.minor, self.patch)


class VersionTypeError(CMDBError):
    """
    Error if update step input was wrong
    """

    def __init__(self, level, update_input):
        super().__init__()
        self.message = 'The version type {1} update for {0} is wrong'.format(level, update_input)


class NoVersionError(CMDBError):
    """
    Error if object from dao child class has no version number
    """

    def __init__(self, public_id):
        super().__init__()
        self.message = 'The object (ID: {}) has no version control'.format(public_id)


class NoPublicIDError(CMDBError):
    """
    Error if object has no public key and public key was'n removed over IGNORED_INIT_KEYS
    """

    def __init__(self):
        super().__init__()
        self.message = 'The object has no general public id - look at the IGNORED_INIT_KEYS constant or the docs'


class NoLogInstance(CMDBError):
    def __init__(self):
        super().__init__()
        self.message = 'Empty logs or class with no log implementation'


class RequiredInitKeyNotFoundError(CMDBError):
    """
    Error if on of the given parameters is missing inside required init keys
    """

    def __init__(self, key_name):
        self.message = 'Following initialization key was not found inside the document: {}'.format(key_name)
