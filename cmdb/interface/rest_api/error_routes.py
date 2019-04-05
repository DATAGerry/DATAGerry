from flask import Blueprint, jsonify, request

error_pages = Blueprint('error_pages', __name__)


@error_pages.errorhandler(400)
def bad_request(error):
    message = {
        'status': 400,
        'response': 'Bad Request: ' + request.url,
        'message': 'The request message had an incorrect structure'
    }
    resp = jsonify(message)
    resp.status_code = 400
    resp.error = error
    return resp


@error_pages.errorhandler(401)
def unauthorized_user(error):
    message = {
        'status': 401,
        'response': 'Unauthorized: ' + request.url,
        'message': 'The request cannot be executed without valid authentication. '
                   'How the authentication is to be performed is transmitted in the '
                   'WWW-Authenticate" header field of the reply.'
    }
    resp = jsonify(message)
    resp.status_code = 401
    resp.error = error
    return resp


@error_pages.errorhandler(403)
def forbidden(error):
    message = {
        'status': 403,
        'response': 'Forbidden: ' + request.url,
        'message': 'The request was not executed because the client was not authorized, for example, '
                   'because the authenticated user is not authorized, or a URL configured as HTTPS '
                   'was called only with HTTP.y.'
    }
    resp = jsonify(message)
    resp.status_code = 403
    resp.error = error
    return resp


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


@error_pages.errorhandler(410)
def page_gone(error):
    """

    :param error: error code
    :return: error page
    """
    message = {
        'status': 410,
        'response': 'Gone: ' + request.url,
        'message': 'The requested resource is no longer provided and has been permanently removed.'
    }
    resp = jsonify(message)
    resp.status_code = 410
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


@error_pages.errorhandler(501)
def not_implemented(error):
    message = {
        'status': 501,
        'response': 'Not Implemented ' + request.url,
        'message': 'The server either does not recognize the request method, or it lacks the '
                   'ability to fulfil the request. Usually this implies future availability '
                   '(e.g., a new feature of a web-service API)'
    }
    resp = jsonify(message)
    resp.status_code = 501
    resp.error = error
    return resp
