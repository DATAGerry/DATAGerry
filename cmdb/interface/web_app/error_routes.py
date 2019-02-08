"""
Error handlers for web_app module
"""

from flask import Blueprint
from flask import render_template
from cmdb.utils.logger import get_logger

LOGGER = get_logger()

error_pages = Blueprint('error_pages', __name__, template_folder='templates')


@error_pages.errorhandler(400)
def bad_request(error):
    """
    The request message had an incorrect structure.
    :param error: error code
    :return: error page
    """
    return render_template('errors/default.html', error=error), 400


@error_pages.errorhandler(401)
def unauthorized_user(error):
    """
    The request cannot be executed without valid authentication.
    How the authentication is to be performed is transmitted in the
    "WWW-Authenticate" header field of the reply.
    :param error: error code
    :return: error page
    """
    return render_template('errors/default.html', error=error), 401


@error_pages.errorhandler(403)
def forbidden(error):
    """
    The request was not executed because the client was not authorized,
    for example, because the authenticated user is not authorized,
    or a URL configured as HTTPS was called only with HTTP.
    :param error: error code
    :return: error page
    """
    return render_template('errors/default.html', error=error), 403


@error_pages.errorhandler(404)
def page_not_found(error):
    """
    The requested resource was not found. This status code can
    also be used to reject a request without further reason.
    :param error: error code
    :return: error page
    """
    return render_template('errors/default.html', error=error), 404


@error_pages.errorhandler(410)
def page_gone(error):
    """
    The requested resource is no longer provided and has been permanently removed.
    :param error: error code
    :return: error page
    """
    return render_template('errors/default.html', error=error), 410


@error_pages.errorhandler(418)
def iam_a_teapot(error):
    """
    This code is to be understood as an April Fool of the IETF.
    Within a joking protocol of coffee making, the Hyper Text Coffee Pot Control Protocol,
    it indicates that a teapot was mistakenly used instead of a coffee pot.
    :param error: error code
    :return: error page
    """
    return render_template('errors/bad_behavior.html', error=error), 418


@error_pages.errorhandler(500)
def internal_server_error(error):
    """
    This is a collective status code for unexpected server errors.
    :param error: error code
    :return: error page
    """
    return render_template('errors/bad_behavior.html', error=error), 500


@error_pages.errorhandler(501)
def not_implemented_error(error):
    """
    The functionality to process the request is not provided by this server.
    For example, the cause is an unknown or unsupported HTTP method.

    Args:
        error: error code

    Returns: error page

    """
    return render_template('errors/default.html', error=error), 501
