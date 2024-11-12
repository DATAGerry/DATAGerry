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
"""TODO: document"""
import json
import logging
from datetime import datetime, timezone
from flask import abort, request, current_app

from cmdb.manager.manager_provider_model.manager_provider import ManagerProvider
from cmdb.manager.manager_provider_model.manager_type_enum import ManagerType
from cmdb.manager.query_builder.builder_parameters import BuilderParameters
from cmdb.manager.security_manager import SecurityManager
from cmdb.manager.users_manager import UsersManager

from cmdb.framework.results import IterationResult
from cmdb.models.user_model.user import UserModel
from cmdb.interface.route_utils import insert_request_user
from cmdb.interface.rest_api.responses.response_parameters.collection_parameters import CollectionParameters
from cmdb.interface.blueprint import APIBlueprint
from cmdb.interface.rest_api.responses import DeleteSingleResponse,\
                                              UpdateSingleResponse,\
                                              InsertSingleResponse,\
                                              GetMultiResponse,\
                                              GetSingleResponse

from cmdb.errors.manager import ManagerGetError, \
                                ManagerInsertError, \
                                ManagerUpdateError, \
                                ManagerDeleteError, \
                                ManagerIterationError
from cmdb.errors.manager.user_manager import UserManagerGetError
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

users_blueprint = APIBlueprint('users', __name__)

# --------------------------------------------------- CRUD - CREATE -------------------------------------------------- #

@users_blueprint.route('/', methods=['POST'])
@insert_request_user
@users_blueprint.protect(auth=True, right='base.user-management.user.add')
@users_blueprint.validate(UserModel.SCHEMA)
def insert_user(data: dict, request_user: UserModel):
    """
    HTTP `POST` route to insert a user into the database

    Args:
        data (UserModel.SCHEMA): Insert data of a new user
    Raises:
        ManagerGetError: If the inserted user could not be found after inserting
        ManagerInsertError: If something went wrong during insertion
    Returns:
        InsertSingleResponse: Insert response with the new user and the corresponding public_id
    """
    users_manager: UsersManager = ManagerProvider.get_manager(ManagerType.USERS_MANAGER, request_user)
    security_manager: SecurityManager = ManagerProvider.get_manager(ManagerType.SECURITY_MANAGER, request_user)

    #REFATOR-FIX
    try:
        user_password = data['password']
        data['password'] = security_manager.generate_hmac(data['password'])
        data['registration_time'] = datetime.now(timezone.utc)

        try:
            if current_app.cloud_mode:
                # Confirm database is available from the request
                data['database'] = request_user.database
        except KeyError:
            return abort(400, "The database could not be retrieved!")

        try:
            if current_app.cloud_mode:
                # Confirm an email was provided when creating the user
                user_email = data['email']

                if not user_email:
                    raise KeyError
        except KeyError:
            LOGGER.debug("[insert_user] No email was provided!")
            return abort(400, "The email is mandatory to create a new user!")

        # Check if email is already exists
        try:
            if current_app.cloud_mode:
                user_with_given_email = users_manager.get_user_by({'email': user_email})

                if user_with_given_email:
                    return abort(400, "The email is already in use!")
        except ManagerGetError:
            pass

        if current_app.cloud_mode:
            # Open file and check if user exists
            with open('etc/test_users.json', 'r', encoding='utf-8') as users_file:
                users_data = json.load(users_file)

                if user_email in users_data:
                    return abort(400, "A user with this email already exists!")

            # Create the user in the dict
            users_data[user_email] = {
                "user_name": data["user_name"],
                "password": user_password,
                "email": data["email"],
                "database": data["database"]
            }

            with open('etc/test_users.json', 'w', encoding='utf-8') as cur_users_file:
                json.dump(users_data, cur_users_file, ensure_ascii=False, indent=4)

        result_id = users_manager.insert_user(data)

        #Confirm that user is created
        user = users_manager.get_user(result_id)
    except ManagerGetError as err:
        #ERROR-FIX
        LOGGER.debug("[insert_user] ManagerGetError: %s", err.message)
        return abort(404, "An error occured when creating the user!")
    except ManagerInsertError as err:
        LOGGER.debug("[insert_user] ManagerInsertError: %s", err.message)
        return abort(400, "Could not create the user in database!")

    api_response = InsertSingleResponse(UserModel.to_dict(user), result_id)

    return api_response.make_response()

# ---------------------------------------------------- CRUD - READ --------------------------------------------------- #

@users_blueprint.route('/', methods=['GET', 'HEAD'])
@insert_request_user
@users_blueprint.protect(auth=True, right='base.user-management.user.view')
@users_blueprint.parse_collection_parameters()
def get_users(params: CollectionParameters, request_user: UserModel):
    """
    HTTP `GET`/`HEAD` route for getting a iterable collection of resources.

    Args:
        params (CollectionParameters): Passed parameters over the http query string
    Returns:
        GetMultiResponse: Which includes a IterationResult of the UserModel.
    Notes:
        Calling the route over HTTP HEAD method will result in an empty body.
    Raises:
        ManagerIterationError: If the collection could not be iterated.
        ManagerGetError: If the collection/resources could not be found.
    """
    users_manager: UsersManager = ManagerProvider.get_manager(ManagerType.USERS_MANAGER, request_user)

    builder_params = BuilderParameters(**CollectionParameters.get_builder_params(params))

    try:
        iteration_result: IterationResult[UserModel] = users_manager.iterate(builder_params)
        users = [UserModel.to_dict(user) for user in iteration_result.results]

        api_response = GetMultiResponse(users,
                                        total=iteration_result.total,
                                        params=params,
                                        url=request.url,
                                        body=request.method == 'HEAD')
    except ManagerIterationError:
        #ERROR-FIX
        return abort(400)
    except ManagerGetError:
        #ERROR-FIX
        return abort(404)

    return api_response.make_response()


@users_blueprint.route('/<int:public_id>', methods=['GET', 'HEAD'])
@insert_request_user
@users_blueprint.protect(auth=True, right='base.user-management.user.view', excepted={'public_id': 'public_id'})
def get_user(public_id: int, request_user: UserModel):
    """
    HTTP `GET`/`HEAD` route for a single user resource.

    Args:
        public_id (int): Public ID user.

    Raises:
        ManagerGetError: When the selected user does not exists.

    Notes:
        Calling the route over HTTP HEAD method will result in an empty body.

    Returns:
        GetSingleResponse: Which includes the json data of a UserModel.
    """
    users_manager: UsersManager = ManagerProvider.get_manager(ManagerType.USERS_MANAGER, request_user)

    try:
        user: UserModel = users_manager.get_user(public_id)
    except UserManagerGetError:
        #MESSAGE-FIX
        return abort(404)

    api_response = GetSingleResponse(UserModel.to_dict(user), body=request.method == 'HEAD')

    return api_response.make_response()

# --------------------------------------------------- CRUD - UPDATE -------------------------------------------------- #

@users_blueprint.route('/<int:public_id>', methods=['PUT', 'PATCH'])
@insert_request_user
@users_blueprint.protect(auth=True, right='base.user-management.user.edit', excepted={'public_id': 'public_id'})
@users_blueprint.validate(UserModel.SCHEMA)
def update_user(public_id: int, data: dict, request_user: UserModel):
    """
    HTTP `PUT`/`PATCH` route for update a single user resource.

    Args:
        public_id (int): Public ID of the updatable user.
        data (UserModel.SCHEMA): New user data to update.
    Raises:
        ManagerGetError: When the user with the `public_id` was not found.
        ManagerUpdateError: When something went wrong during the update.
    Returns:
        UpdateSingleResponse: With update result of the new updated user.
    """
    users_manager: UsersManager = ManagerProvider.get_manager(ManagerType.USERS_MANAGER, request_user)

    try:
        user = UserModel.from_data(data=data)
        users_manager.update_user(public_id, user)

        api_response = UpdateSingleResponse(UserModel.to_dict(user))
    except ManagerGetError:
        #ERROR-FIX
        return abort(404)
    except ManagerUpdateError as err:
        LOGGER.debug("[update_user] ManagerUpdateError: %s", err.message)
        return abort(400, f"User with piblic_id: {public_id} could not be updated!")

    return api_response.make_response()


@users_blueprint.route('/<int:public_id>/password', methods=['PATCH'])
@insert_request_user
@users_blueprint.protect(auth=True, right='base.user-management.user.edit', excepted={'public_id': 'public_id'})
def change_user_password(public_id: int, request_user: UserModel):
    """
    HTTP `PATCH` route for updating a single user password.

    Args:
        public_id (int): Public ID of the user.
    Raises:
        ManagerGetError: When the user with the `public_id` was not found.
        ManagerUpdateError: When something went wrong during the updated.
    Returns:
        UpdateSingleResponse: User with new password
    """
    users_manager: UsersManager = ManagerProvider.get_manager(ManagerType.USERS_MANAGER, request_user)
    security_manager: SecurityManager = ManagerProvider.get_manager(ManagerType.SECURITY_MANAGER, request_user)

    try:
        user = users_manager.get_user(public_id)
    except UserManagerGetError:
        #MESSAGE-FIX
        return abort(404)

    try:
        password = security_manager.generate_hmac(request.json.get('password'))
        user.password = password
        users_manager.update_user(public_id, user)
        api_response = UpdateSingleResponse(UserModel.to_dict(user))
    except ManagerGetError:
        #ERROR-FIX
        return abort(404)
    except ManagerUpdateError as err:
        LOGGER.debug("[change_user_password] ManagerUpdateError: %s", err.message)
        return abort(400, f"Password for user with public_id: {public_id} could not be changed!")

    return api_response.make_response()

# --------------------------------------------------- CRUD - DELETE -------------------------------------------------- #

@users_blueprint.route('/<int:public_id>', methods=['DELETE'])
@insert_request_user
@users_blueprint.protect(auth=True, right='base.user-management.user.delete')
def delete_user(public_id: int, request_user: UserModel):
    """
    HTTP `DELETE` route for delete a single user resource.

    Args:
        public_id (int): Public ID of the user.
    Raises:
        ManagerGetError: When the user with the `public_id` was not found.
        ManagerDeleteError: When something went wrong during the deletion.
    Returns:
        DeleteSingleResponse: Delete result with the deleted user as data.
    """
    users_manager: UsersManager = ManagerProvider.get_manager(ManagerType.USERS_MANAGER, request_user)

    try:
        deleted_group = users_manager.delete_user(public_id)
        api_response = DeleteSingleResponse(raw=UserModel.to_dict(deleted_group))
    except ManagerGetError as err:
        #ERROR-FIX
        LOGGER.debug("[delete_user] ManagerGetError: %s", err.message)
        return abort(404, f"Could not delete user with ID: {public_id} !")
    except ManagerDeleteError as err:
        #ERROR-FIX
        LOGGER.debug("[delete_user] ManagerDeleteError: %s", err.message)
        return abort(404, f"Could not delete user with ID: {public_id} !")

    return api_response.make_response()
