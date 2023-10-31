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

class Config:
    """Parent configuration class."""
    TESTING = False
    DEBUG = False
    ENV = 'production'
    APPLICATION_ROOT = '/'


class DevelopmentConfig(Config):
    """Configurations for Development."""
    DEBUG = True
    ENV = 'development'


class ProductionConfig(Config):
    """Configurations for Production."""
    DEBUG = False
    TESTING = False
    ENV = 'production'


class TestingConfig(Config):
    """Configurations for Production."""
    DEBUG = True
    TESTING = True
    ENV = 'testing'


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}
