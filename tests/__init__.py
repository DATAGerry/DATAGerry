"""
CMDB test module

Tested modules:
    - cmdb_object_framework in test_object_framework
    - data_storage in test_data_storage
    - plugins in test_plugins
    - user_management in test_user_management
    - cmdb_render in test_render
"""

import cmdb
cmdb.__MODE__ = 'TESTING'
