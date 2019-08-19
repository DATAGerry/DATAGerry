# -*- coding: utf-8 -*-
# dataGerry - OpenSource Enterprise CMDB
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

import os

import requests
import requirements
from termcolor import colored


def test_lib_licenses():
    """Test licenses of libraries
    
    This test will parse the requirements.txt and get the license
    of each used library, which will be matched against a list of
    approved licenses.
    """

    # config parameters
    req_filename = os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../requirements.txt"))
    pypi_baseurl = "https://pypi.org/pypi/{}/json"
    approved_licenses = [
        "MIT",
        "BSD",
        "Apache",
        "Dual License",
        "Artistic License",
        "GPL license with a special exception which allows to use PyInstaller"
    ]

    # default values
    result = True

    # debug output
    print("approved licenses: {}".format(approved_licenses))

    # open requirements.txt file
    with open(req_filename, 'r') as req_file:

        # parse each line of requirements file
        for req in requirements.parse(req_file):
            pypi_url = pypi_baseurl.format(req.name)
            pypi_response = requests.get(pypi_url)
            pypi_data = pypi_response.json()
            pypi_license = pypi_data["info"]["license"]
            output = ""
            if not any(license in pypi_license for license in approved_licenses):
                output = colored("✘ {}:{}".format(req.name, pypi_license), "red")
                result = False
            else:
                output = "✓ {}:{}".format(req.name, pypi_license)
            print(output)

    # check result
    assert result
