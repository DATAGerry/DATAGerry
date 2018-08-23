from flask import Blueprint, jsonify, request

error_pages = Blueprint('error_pages', __name__)


@error_pages.errorhandler(404)
def page_not_found(error):
    message = {
        'status': 404,
        'response': 'Not Found: ' + request.url,
        'message': 'The requested URL was not found on the server. If you entered the URL manually please check your '
                   'spelling and try again.'
    }
    resp = jsonify(message)
    resp.status_code = 404
    resp.error = error
    return resp


@error_pages.errorhandler(405)
def method_not_allowed(error):
    message = {
        'status': 405,
        'response': 'Method Not Allowed: ' + request.url,
        'message': 'A request was made with a method that is not supported for the requested URL.The Allow header '
                   'should be included in the response to tell the client what methods are allowed on the requested '
                   'resource.'
    }
    resp = jsonify(message)
    resp.status_code = 405
    resp.error = error
    return resp


@error_pages.errorhandler(406)
def not_acceptable(error):
    message = {
        'status': 406,
        'response': 'Not Acceptable: ' + request.url,
        'message': 'The resource identified by the request is only capable of generating response entities which have '
                   'content characteristics not acceptable according to the accept headers sent in the request.'
    }
    resp = jsonify(message)
    resp.status_code = 406
    resp.error = error
    return resp


@error_pages.errorhandler(409)
def conflict(error, cmdb_error):
    message = {
        'status': 409,
        'response': 'Conflict: ' + request.url,
        'message': 'Conflict',
        'cmdb_error': cmdb_error
    }
    resp = jsonify(message)
    resp.status_code = 409
    resp.error = error
    return resp


@error_pages.errorhandler(500)
def internal_server_error(error):
    message = {
        'status': 500,
        'response': 'Internal Server Error: ' + request.url,
        'message': 'Unknown error'
    }
    resp = jsonify(message)
    resp.status_code = 500
    resp.error = error
    return resp
