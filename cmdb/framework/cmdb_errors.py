# DATAGERRY - OpenSource Enterprise CMDB
# Copyright (C) 2023 becon GmbH
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
"""TODO: document"""
from cmdb.framework.cmdb_base import ManagerInitError, ManagerGetError, ManagerInsertError, ManagerUpdateError, \
    ManagerDeleteError
from cmdb.utils.error import CMDBError
# -------------------------------------------------------------------------------------------------------------------- #

class WrongInputFormatError(CMDBError):
    """TODO: document"""
    def __init__(self, class_name, data, error):
        self.message = f"Error while parsing {class_name} - Data: {data} - Error: {error}"


class UpdateError(CMDBError):
    """TODO: document"""
    def __init__(self, class_name, data, error):
        self.message = f"Update error while updating {class_name} - Data: {data} - Error: {error}"


class TypeInsertError(CMDBError):
    """TODO: document"""
    def __init__(self, type_id):
        self.message = f"Type with ID: {type_id} could not be inserted!"


class TypeAlreadyExists(CMDBError):
    """TODO: document"""
    def __init__(self, type_id):
        self.message = f"Type with ID: {type_id} already exists!"


class TypeNotFoundError(CMDBError):
    """TODO: document"""
    def __init__(self, type_id):
        self.message = f"Type with ID: {type_id} not found!"


class ObjectNotFoundError(CMDBError):
    """TODO: document"""
    def __init__(self, obj_id):
        self.message = f"Object with ID: {obj_id} not found!"


class ObjectInsertError(CMDBError):
    """TODO: document"""
    def __init__(self, error):
        self.message = f'Object could not be inserted | Error {error.message} \n show into logs for details'


class ObjectUpdateError(CMDBError):
    """TODO: document"""
    def __init__(self, msg):
        self.message = f'Something went wrong during update: {msg}'


class ObjectDeleteError(CMDBError):
    """TODO: document"""
    def __init__(self, msg):
        self.message = f'Something went wrong during delete: {msg}'


class NoRootCategories(CMDBError):
    """TODO: document"""
    def __init__(self):
        self.message = 'No root categories exists'


class ExternalFillError(CMDBError):
    """Error if href of TypeExternalLink could not filled with input data"""
    def __init__(self, inputs, error):
        super().__init__()
        self.message = f'Href link do not fit with inputs: {inputs}, error: {error}'


class TypeReferenceLineFillError(CMDBError):
    """Error if summary line of TypeReferences could not filled with input data"""
    def __init__(self, inputs, error):
        super().__init__()
        self.message = f'Type reference summary line do not fit with inputs: {inputs}, error: {error}'


class FieldInitError(CMDBError):
    """Error if field could not be initialized"""
    def __init__(self, field_name):
        super().__init__()
        self.message = f'Field {field_name} could not be initialized'


class NoSummaryDefinedError(CMDBError):
    """Error if no summary fields designed"""
    def __init__(self, field_name):
        super().__init__()
        self.message = f'Field {field_name} could not be initialized'


class FieldNotFoundError(CMDBError):
    """Error if field do not exists"""

    def __init__(self, field_name, type_name):
        super().__init__()
        self.message = f'Field {field_name} was not found inside input_type: {type_name}'

# ---------------------------------------------------------------------------- #
#                              LOCATION EXCEPTIONS                             #
# ---------------------------------------------------------------------------- #
class LocationManagerError(ManagerGetError):
    """TODO: document"""
    def __init__(self, err):
        super().__init__(err=err)


class LocationManagerInitError(ManagerInitError):
    """TODO: document"""
    def __init__(self, err):
        super().__init__(err=err)


class LocationManagerGetError(ManagerGetError):
    """TODO: document"""
    def __init__(self, err):
        super().__init__(err=err)


class LocationManagerInsertError(ManagerInsertError):
    """TODO: document"""
    def __init__(self, err):
        super().__init__(err=err)

class LocationManagerUpdateError(ManagerUpdateError):
    """TODO: document"""
    def __init__(self, err):
        super().__init__(err=err)

class LocationManagerDeleteError(ManagerDeleteError):
    """TODO: document"""
    def __init__(self, err):
        super().__init__(err=err)


# -------------------------------------------------------------------------------------------------------------------- #
#                                                   OBJECT EXCEPTIONS                                                  #
# -------------------------------------------------------------------------------------------------------------------- #

class ObjectManagerInitError(ManagerInitError):
    """TODO: document"""
    def __init__(self, err):
        super().__init__(err=err)


class ObjectManagerGetError(ManagerGetError):
    """TODO: document"""
    def __init__(self, err):
        super().__init__(err=err)

class ObjectManagerInsertError(ManagerInsertError):
    """TODO: document"""
    def __init__(self, err):
        super().__init__(err=err)


class ObjectManagerUpdateError(ManagerUpdateError):
    """TODO: document"""
    def __init__(self, err):
        super().__init__(err=err)


class ObjectManagerDeleteError(ManagerDeleteError):
    """TODO: document"""
    def __init__(self, err):
        super().__init__(err=err)



# -------------------------------------------------------------------------------------------------------------------- #
#                                              SECTION TEMPLATE EXCEPTIONS                                             #
# -------------------------------------------------------------------------------------------------------------------- #

class SectionTemplateManagerError(ManagerGetError):
    """TODO: document"""
    def __init__(self, err):
        super().__init__(err=err)


class SectionTemplateManagerInitError(ManagerInitError):
    """TODO: document"""
    def __init__(self, err):
        super().__init__(err=err)


class SectionTemplateManagerGetError(ManagerGetError):
    """TODO: document"""
    def __init__(self, err):
        super().__init__(err=err)


class SectionTemplateManagerInsertError(ManagerInsertError):
    """TODO: document"""
    def __init__(self, err):
        super().__init__(err=err)

class SectionTemplateManagerUpdateError(ManagerUpdateError):
    """TODO: document"""
    def __init__(self, err):
        super().__init__(err=err)

class SectionTemplateManagerDeleteError(ManagerDeleteError):
    """TODO: document"""
    def __init__(self, err):
        super().__init__(err=err)