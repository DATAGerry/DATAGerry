from cmdb.utils.error import CMDBError


class WrongInputFormatError(CMDBError):
    def __init__(self, class_name, data, error):
        self.message = 'Error while parsing {} - Data: {} - Error: '.format(class_name, data, error)


class UpdateError(CMDBError):
    def __init__(self, class_name, data, error):
        self.message = 'Update error while updating {} - Data: {} - Error: '.format(class_name, data, error)


class TypeInsertError(CMDBError):
    def __init__(self, type_id):
        self.message = 'Type with ID: {} could not be inserted!'.format(type_id)


class TypeAlreadyExists(CMDBError):
    def __init__(self, type_id):
        self.message = 'Type with ID: {} already exists!'.format(type_id)


class TypeNotFoundError(CMDBError):
    def __init__(self, type_id):
        self.message = 'Type with ID: {} not found!'.format(type_id)


class ObjectInsertError(CMDBError):
    def __init__(self, error):
        self.message = 'Object could not be inserted | Error {} \n show into logs for details'.format(error.message)


class ObjectUpdateError(CMDBError):
    def __init__(self, msg):
        self.message = 'Something went wrong during update: {}'.format(msg)


class NoRootCategories(CMDBError):
    def __init__(self):
        self.message = 'No root categories exists'


class ExternalFillError(CMDBError):
    """Error if href of _ExternalLink could not filled with input data"""

    def __init__(self, inputs, error):
        super().__init__()
        self.message = 'Href link do not fit with inputs: {}, error: {}'.format(inputs, error)


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