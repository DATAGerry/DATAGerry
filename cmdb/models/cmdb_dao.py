# DataGerry - OpenSource Enterprise CMDB
# Copyright (C) 2026 becon GmbH
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
# along with this program. If not, see <https://www.gnu.org/licenses/>.
"""
Implementation of CmdbDAO
"""
from logging import Logger, getLogger
from typing import Type, TypeVar, Any
from enum import Enum
import pprint

from pymongo import IndexModel

from cmdb.models.cmdb_versioning import Versioning

from cmdb.errors.cmdb_object import NoPublicIDError, NoVersionError, RequiredInitKeyNotFoundError
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER: Logger = getLogger(__name__)

T = TypeVar("T", bound="CmdbDAO")

# -------------------------------------------------------------------------------------------------------------------- #
#                                                    CmdbDAO - CLASS                                                   #
# -------------------------------------------------------------------------------------------------------------------- #
class CmdbDAO:
    """
    The data access object is the basic presentation if objects and their necessary dependent classes are to be stored
    in the database

    Attributes:
        DAO_ASCENDING (int): models sort order ascending
        DAO_DESCENDING (int): models sort order descending
        COLLECTION (str): name of the database table - should always be overwritten
        REQUIRED_INIT_KEYS (list, optional): list of default parameters which an object needs to work.
            __new__ refuses a construction that omits one, and for a model sharing from_data below it
            is also the list of keys a DOCUMENT must carry - which is how a model keeps the strictness
            of reading a key with data['key'] instead of data.get('key')
        DATE_FIELDS (tuple, optional): names of the document's date-typed fields. A model declaring
            them opts its collection into date normalisation: GenericManager coerces exactly these
            keys into real BSON dates on every write path that hands it a raw dict, so a date is
            never stored as the Mongo extended-JSON wrapper the frontend sends. Empty by default,
            which leaves every other collection untouched
        KEYS (type[Enum], optional): the enum naming the document's keys. A model that declares it,
            plus its two error types, inherits the shared from_data / to_json below and writes
            neither of its own - see their docstrings for what that requires. None by default, which
            leaves a model with its own hand-written pair
        INIT_FROM_DATA_ERROR (type[Exception], optional): the error the shared from_data raises
        TO_JSON_ERROR (type[Exception], optional): the error the shared to_json raises
        VERSIONING_MAJOR (int): addend for major version updates
        VERSIONING_MINOR (int): addend for minor version updates
        VERSIONING_PATCH (int): addend for small patches

    Note:
        COLLECTION and REQUIRED_INIT_KEYS should always be overwritten by inherited classes
    """

    DAO_ASCENDING = 1
    DAO_DESCENDING = -1
    COLLECTION = 'framework.*'
    SCHEMA: dict[str, Any] = {}

    # The one key every document carries, and the only one the shared to_json reads through an
    # accessor instead of an attribute
    PUBLIC_ID_KEY: str = 'public_id'

    SUPER_INIT_KEYS: list[str] = [
        PUBLIC_ID_KEY
    ]

    SUPER_INDEX_KEYS: list[dict[str, Any]] = [
        {
            'keys': [(PUBLIC_ID_KEY, DAO_ASCENDING)],
            'name': PUBLIC_ID_KEY,
            'unique': True
        }
    ]

    REQUIRED_INIT_KEYS: list[str] = []
    INDEX_KEYS: list[dict[str, Any]] = []
    DATE_FIELDS: tuple[str, ...] = ()
    KEYS: type[Enum] | None = None
    INIT_FROM_DATA_ERROR: type[Exception] | None = None
    TO_JSON_ERROR: type[Exception] | None = None
    VERSIONING_MAJOR = 2
    VERSIONING_MINOR = 1
    VERSIONING_PATCH = 0


    def __init__(self, public_id : int, **kwargs: Any) -> None:
        """
        All parameters inside *kwargs will be auto convert to attributes

        Args:
            **kwargs: list of parameters
        """
        self.public_id: int = int(public_id)

        for key, value in kwargs.items():
            if key == 'version':
                self.version = value
            else:
                setattr(self, key, value)


    def __new__(cls, *args: Any, **kwargs: Any):
        """
        auto call function by object initialization
        checks if all required keys for cmdb usage are present
        @deprecated_implementation
        if not all(key in key_list for key in cls.REQUIRED_INIT_KEYS):

        Returns:
            Instance of the object

        Raises:
            RequiredInitKeyNotFoundError: if some given attributes are not inside the requirement lists
        """
        init_keys: list[str] = cls.SUPER_INIT_KEYS + cls.REQUIRED_INIT_KEYS

        for req_key in init_keys:
            if req_key in kwargs:
                continue

            raise RequiredInitKeyNotFoundError(f"A required InitKey is missing: {req_key}!")

        return super().__new__(cls)


    def get_public_id(self) -> int:
        """
        get the public id of current element

        Note:
            Since the models object is not initializable
            the child class object will inherit this function
            SHOULD NOT BE OVERWRITTEN!

        Raises:
            NoPublicIDError: if `public_id` is zero or not set

        Returns:
            int: public id
        """
        if self.public_id == 0:
            raise NoPublicIDError("No public_id assigned!")

        return self.public_id


    @classmethod
    def get_index_keys(cls) -> list[IndexModel]:
        """
        Retrieves a list of index models based on class-defined index keys

        Returns:
            list: A list of IndexModel instances created from `INDEX_KEYS` and `SUPER_INDEX_KEYS`
        """
        return [IndexModel(**index) for index in cls.INDEX_KEYS + cls.SUPER_INDEX_KEYS]


    def update_version(self, update: int) -> str:
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
            raise NoVersionError(f"The object (ID: {self.get_public_id()}) has no version property")

        updater_version = Versioning(*map(int, self.version.split('.')))

        if update == self.VERSIONING_MAJOR:
            updater_version.update_major()
        elif update == self.VERSIONING_MINOR:
            updater_version.update_minor()
        else:
            updater_version.update_patch()

        return repr(updater_version)


    def get_version(self) -> str:
        """
        Get version number if exists
        Returns:
            version number

        Raiser:
            NoVersionError: If not self.version
        """
        if self.version:
            return self.version

        raise NoVersionError(f"The object (ID: {self.get_public_id()}) has no version property")


    def __repr__(self) -> str:
        return f'Class: {self.__class__.__name__} \nDict:\n{pprint.pformat(self.__dict__)}'


    @classmethod
    def normalize_document(cls, data: dict[str, Any]) -> None:
        """
        Normalises a raw document IN PLACE before the shared from_data reads it

        The hook for the per-field rules a key list cannot express - a date that arrives as the Mongo
        extended-JSON wrapper, a two-state boolean stored as null. Does nothing by default, so a model
        whose keys need no massaging declares nothing.

        Args:
            data (dict[str, Any]): The document or validated payload, edited in place
        """


    @classmethod
    def from_data(cls: Type[T], data: dict[str, Any]) -> T:
        """
        Initialises the model from a document

        Shared by every model that declares ``KEYS``: the key enum names the constructor arguments,
        which is what lets one implementation serve them all. Two things it therefore requires of such
        a model - both of them true of every ISMS entity - are that each key is an ``__init__``
        parameter of the same name, and that the constructor is the only place a value is massaged
        (``threats or []``), with ``normalize_document`` for whatever has to happen to the raw
        document first.

        ``REQUIRED_INIT_KEYS`` names the keys the document itself must carry: a model that used to read
        them with ``data['key']`` keeps that strictness by declaring them, and a document missing one is
        refused rather than turned into an instance holding None.

        A model that declares no ``KEYS`` must implement this itself; the ISMS family is the group
        that shares it, and collapsing eleven copies of it is what retired thirty untested
        ``except`` arms.

        Args:
            data (dict[str, Any]): The document to initialise from

        Raises:
            NotImplementedError: If the model neither declares KEYS nor implements from_data
            INIT_FROM_DATA_ERROR: The model's own error, if the initialisation fails

        Returns:
            T: The model instance carrying the document's values
        """
        if cls.KEYS is None:
            raise NotImplementedError(f"{cls.__name__} must implement a 'from_data' method!")

        # The declared types carry None for a model that shares neither method; the guard above is what
        # makes the enum iterable and the error class callable from here on
        # pylint: disable=not-an-iterable,not-callable
        try:
            cls.normalize_document(data)

            missing_keys: list[str] = [key for key in cls.REQUIRED_INIT_KEYS if key not in data]

            if missing_keys:
                raise KeyError(f"Document is missing the required key(s): {missing_keys}!")

            return cls(**{key.value: data.get(key.value) for key in cls.KEYS})
        except Exception as err:
            raise cls.INIT_FROM_DATA_ERROR(err) from err


    @classmethod
    def to_json(cls: Type[T], instance: "CmdbDAO") -> dict[str, Any]:
        """
        Converts the model into a json compatible dict

        Shared by every model that declares ``KEYS``, and the closure that makes the key set a real
        contract: the payload is exactly the enum's keys, so a value stored outside them cannot reach
        a response and a key removed from the enum cannot linger in one. ``public_id`` is read through
        ``get_public_id()`` - the accessor that refuses an unassigned id - and every other key through
        the attribute of the same name.

        The instance is type-checked first, which matters more than it looks: two models with the same
        field names serialise as each other without complaint, and the ISMS scale entities are exactly
        that (IsmsImpact and IsmsLikelihood both carry name / calculation_basis / description).

        Args:
            instance (CmdbDAO): The model instance to convert

        Raises:
            NotImplementedError: If the model neither declares KEYS nor implements to_json
            TO_JSON_ERROR: The model's own error, if the conversion fails

        Returns:
            dict[str, Any]: Json compatible dict of the instance's values
        """
        if cls.KEYS is None:
            raise NotImplementedError(f"{cls.__name__} must implement a 'to_json' method!")

        # See from_data: the guard above narrows both declared types
        # pylint: disable=not-an-iterable,not-callable
        try:
            # Structurally identical models exist - IsmsImpact and IsmsLikelihood carry the very same
            # four keys - so without this check one serialises cleanly as the other and the mix-up
            # reaches the response looking valid
            if not isinstance(instance, cls):
                raise TypeError(f"Expected {cls.__name__} in 'to_json' got: {type(instance).__name__}!")

            return {
                key.value: instance.get_public_id() if key.value == cls.PUBLIC_ID_KEY
                else getattr(instance, key.value)
                for key in cls.KEYS
            }
        except Exception as err:
            raise cls.TO_JSON_ERROR(err) from err
