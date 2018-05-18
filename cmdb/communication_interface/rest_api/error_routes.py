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

