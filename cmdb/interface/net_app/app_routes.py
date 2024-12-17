# DATAGERRY - OpenSource Enterprise CMDB
# Copyright (C) 2024 becon GmbH
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
Blueprint for datagerry-app routes
"""
import logging
from flask import Blueprint
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

app_pages = Blueprint("app_pages", __name__, static_folder="datagerry-app", static_url_path="")


@app_pages.route('/')
def default_page():
    """TODO: document"""
    return app_pages.send_static_file("index.html")


@app_pages.errorhandler(404)
def redirect_index(error):
    """TODO: document"""
    LOGGER.debug("[redirect_index] Error: %s", error)
    return app_pages.send_static_file("index.html")
