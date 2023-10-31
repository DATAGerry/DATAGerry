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
from cmdb.framework.cmdb_base import ManagerInitError, ManagerGetError, ManagerInsertError, ManagerUpdateError, \
    ManagerDeleteError
from cmdb.utils.error import CMDBError


class WrongInputFormatError(CMDBError):
    def __init__(self, class_name, data, error):
        self.message = f"Error while parsing {class_name} - Data: {data} - Error: {error}"


class UpdateError(CMDBError):
    def __init__(self, class_name, data, error):
        self.message = f"Update error while updating {class_name} - Data: {data} - Error: {error}"


class TypeInsertError(CMDBError):
    def __init__(self, type_id):
        self.message = f"Type with ID: {type_id} could not be inserted!"


class TypeAlreadyExists(CMDBError):
    def __init__(self, type_id):
        self.message = f"Type with ID: {type_id} already exists!"


class TypeNotFoundError(CMDBError):
    def __init__(self, type_id):
        self.message = f"Type with ID: {type_id} not found!"


class ObjectNotFoundError(CMDBError):
    def __init__(self, obj_id):
        self.message = f"Object with ID: {obj_id} not found!"


class ObjectInsertError(CMDBError):
    def __init__(self, error):
        self.message = 'Object could not be inserted | Error {} \n show into logs for details'.format(error.message)


class ObjectUpdateError(CMDBError):
    def __init__(self, msg):
        self.message = 'Something went wrong during update: {}'.format(msg)


class ObjectDeleteError(CMDBError):
    def __init__(self, msg):
        self.message = 'Something went wrong during delete: {}'.format(msg)


class NoRootCategories(CMDBError):
    def __init__(self):
        self.message = 'No root categories exists'


class ExternalFillError(CMDBError):
    """Error if href of TypeExternalLink could not filled with input data"""

    def __init__(self, inputs, error):
        super().__init__()
        self.message = 'Href link do not fit with inputs: {}, error: {}'.format(inputs, error)


class TypeReferenceLineFillError(CMDBError):
    """Error if summary line of TypeReferences could not filled with input data"""

    def __init__(self, inputs, error):
        super().__init__()
        self.message = 'Type reference summary line do not fit with inputs: {}, error: {}'.format(inputs, error)


class FieldInitError(CMDBError):
    """Error if field could not be initialized"""

    def __init__(self, field_name):
        super().__init__()
        self.message = 'Field {} could not be initialized'.format(field_name)


class NoSummaryDefinedError(CMDBError):
    """Error if no summary fields designed"""

    def __init__(self, field_name):
        super().__init__()
        self.message = 'Field {} could not be initialized'.format(field_name)


class FieldNotFoundError(CMDBError):
    """Error if field do not exists"""

    def __init__(self, field_name, type_name):
        super().__init__()
        self.message = 'Field {} was not found inside input_type: {}'.format(field_name, type_name)

# ---------------------------------------------------------------------------- #
#                              LOCATION EXCEPTIONS                             #
# ---------------------------------------------------------------------------- #
class LocationManagerError(ManagerGetError):

    def __init__(self, err):
        super().__init__(err=err)


class LocationManagerInitError(ManagerInitError):

    def __init__(self, err):
        super().__init__(err=err)


class LocationManagerGetError(ManagerGetError):

    def __init__(self, err):
        super().__init__(err=err)


class LocationManagerInsertError(ManagerInsertError):

    def __init__(self, err):
        super().__init__(err=err)

class LocationManagerUpdateError(ManagerUpdateError):

    def __init__(self, err):
        super().__init__(err=err)

class LocationManagerDeleteError(ManagerDeleteError):

    def __init__(self, err):
        super().__init__(err=err)

# ---------------------------------------------------------------------------- #
#                               OBJECT EXCEPTIONS                              #
# ---------------------------------------------------------------------------- #

class ObjectManagerInitError(ManagerInitError):

    def __init__(self, err):
        super().__init__(err=err)


class ObjectManagerGetError(ManagerGetError):

    def __init__(self, err):
        super().__init__(err=err)

class ObjectManagerInsertError(ManagerInsertError):

    def __init__(self, err):
        super().__init__(err=err)


class ObjectManagerUpdateError(ManagerUpdateError):

    def __init__(self, err):
        super().__init__(err=err)


class ObjectManagerDeleteError(ManagerDeleteError):

    def __init__(self, err):
        super().__init__(err=err)
