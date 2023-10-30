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

"""
This file contans all profile data and logics for the initial assistant
"""
import logging
from enum import Enum

from cmdb.framework.assistant_profiles.profile_user_management import UserManagementProfile
from cmdb.framework.assistant_profiles.profile_location import LocationProfile
from cmdb.framework.assistant_profiles.profile_ipam import IPAMProfile
from cmdb.framework.assistant_profiles.profile_client_management import ClientManagementProfile
from cmdb.framework.assistant_profiles.profile_server_management import ServerManagementProfile
from cmdb.framework.assistant_profiles.profile_network_infrastructure import NetworkInfrastructureProfile

LOGGER = logging.getLogger(__name__)


class ProfileName(str, Enum):
    """
    Enumeration of all valid profile names which can be created through the initial assistant
    
    Args:
        Enum (str): Name of a profile
    """
    USER_MANAGEMENT = 'user-management-profile'
    LOCATION = 'location-profile'
    IPAM = 'ipam-profile'
    CLIENT_MANAGEMENT = 'client-management-profile'
    SERVER_MANAGEMENT = 'server-management-profile'
    NETWORK_INFRASTRUCTURE = 'network-infrastructure-profile'

class ProfileAssistant:
    """
    This class holds all profiles and logics for the initial assistant
    """
# -------------------------------------------------------------------------------------------------------------------- #
#                                                   PROFILE CREATION                                                   #
# -------------------------------------------------------------------------------------------------------------------- #

    def create_profiles(self, profile_list):
        """
        Creates types from profiles in the profile_list

        Args:
            profile_list: List of profiles which should be created
        """
        created_type_ids: dict = {
            'company_id': None,
            'user_id': None,
            'customer_user_id': None,
            'country_id': None,
            'city_id': None,
            'building_id': None,
            'room_id': None,
            'rack_id': None,
            'network_id': None,
            'vlan_id': None,
            'operating_system_id': None,
            'client_id': None,
            'monitor_id': None,
            'printer_id': None,
            'server_id': None,
            'appliance_id': None,
            'virtual_server_id': None,
            'switch_id': None,
            'router_id': None,
            'patch_panel_id': None,
            'wireless_access_point_id': None,
        }

        try:
            # create all types from user management profile
            if ProfileName.USER_MANAGEMENT in profile_list:
                cur_profile = UserManagementProfile(created_type_ids)
                created_type_ids = cur_profile.create_user_management_profile()

            # create all types from location profile
            if ProfileName.LOCATION in profile_list:
                cur_profile = LocationProfile(created_type_ids)
                created_type_ids = cur_profile.create_location_profile()

            # create all types from ipam profile
            if ProfileName.IPAM in profile_list:
                cur_profile = IPAMProfile(created_type_ids)
                created_type_ids = cur_profile.create_ipam_profile()

            # create all types from client management profile
            if ProfileName.CLIENT_MANAGEMENT in profile_list:
                cur_profile = ClientManagementProfile(created_type_ids)
                created_type_ids = cur_profile.create_client_management_profile()

            # create all types from server management profile
            if ProfileName.SERVER_MANAGEMENT in profile_list:
                cur_profile = ServerManagementProfile(created_type_ids)
                created_type_ids = cur_profile.create_server_management_profile()

            # create all types from network infrastructure profile
            if ProfileName.SERVER_MANAGEMENT in profile_list:
                cur_profile = NetworkInfrastructureProfile(created_type_ids)
                created_type_ids = cur_profile.create_network_infrastructure_profile()
        except Exception as error:
            LOGGER.info(f"Assitant Error: {error}")

        created_ids = []

        for type_id in created_type_ids:
            created_ids.append(type_id)

        return created_ids
