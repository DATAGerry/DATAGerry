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

from cmdb.security.security import SecurityManager
from cmdb.user_management.managers.user_manager import UserManager

from cmdb.search import Query
from cmdb.interface.route_utils import insert_request_user
from cmdb.interface.api_parameters import CollectionParameters
from cmdb.interface.blueprint import APIBlueprint
from cmdb.interface.response import GetMultiResponse, \
                                    GetSingleResponse, \
                                    InsertSingleResponse, \
                                    UpdateSingleResponse, \
                                    DeleteSingleResponse, \
                                    ErrorMessage
from cmdb.framework.utils import PublicID
from cmdb.framework.results import IterationResult
from cmdb.user_management import UserModel
from cmdb.manager.manager_provider import ManagerType, ManagerProvider

from cmdb.errors.manager import ManagerGetError, \
                                ManagerInsertError, \
                                ManagerUpdateError, \
                                ManagerDeleteError, \
                                ManagerIterationError
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
    user_manager: UserManager = ManagerProvider.get_manager(ManagerType.USER_MANAGER, request_user)
    security_manager: SecurityManager = ManagerProvider.get_manager(ManagerType.SECURITY_MANAGER, request_user)

    try:
        user_password = data['password']
        data['password'] = security_manager.generate_hmac(data['password'])
        data['registration_time'] = datetime.now(timezone.utc)

        try:
            if current_app.cloud_mode:
                # Confirm database is available from the request
                data['database'] = request_user.database
        except KeyError:
            return ErrorMessage(400, "The database could not be retrieved!").response()

        try:
            if current_app.cloud_mode:
                # Confirm an email was provided when creating the user
                user_email = data['email']

                if not user_email:
                    raise KeyError
        except KeyError:
            LOGGER.debug("[insert_user] No email was provided!")
            return ErrorMessage(400, "The email is mandatory to create a new user!").response()

        # Check if email is already exists
        try:
            if current_app.cloud_mode:
                user_with_given_email = user_manager.get_by(Query({'email': user_email}))

                if user_with_given_email:
                    return ErrorMessage(400, "The email is already in use!").response()
        except ManagerGetError:
            pass

        if current_app.cloud_mode:
            # Open file and check if user exists
            with open('etc/test_users.json', 'r', encoding='utf-8') as users_file:
                users_data = json.load(users_file)

                if user_email in users_data:
                    return ErrorMessage(400, "A user with this email already exists!").response()

            # Create the user in the dict
            users_data[user_email] = {
                "user_name": data["user_name"],
                "password": user_password,
                "email": data["email"],
                "database": data["database"]
            }

            with open('etc/test_users.json', 'w', encoding='utf-8') as cur_users_file:
                json.dump(users_data, cur_users_file, ensure_ascii=False, indent=4)

        result_id: PublicID = user_manager.insert(data)

        #Confirm that user is created
        user = user_manager.get(public_id=result_id)
    except ManagerGetError as err:
        #TODO: ERROR-FIX
        LOGGER.debug("[insert_user] ManagerGetError: %s", err.message)
        return abort(404, "An error occured when creating the user!")
    except ManagerInsertError as err:
        LOGGER.debug("[insert_user] ManagerInsertError: %s", err.message)
        return abort(400, "Could not create the user in database!")
    api_response = InsertSingleResponse(UserModel.to_dict(user), result_id, request.url, UserModel.MODEL)

    return api_response.make_response(prefix='users')

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
    user_manager: UserManager = ManagerProvider.get_manager(ManagerType.USER_MANAGER, request_user)

    try:
        iteration_result: IterationResult[UserModel] = user_manager.iterate(filter=params.filter,
                                                                            limit=params.limit,
                                                                            skip=params.skip,
                                                                            sort=params.sort,
                                                                            order=params.order)
        users = [UserModel.to_dict(user) for user in iteration_result.results]

        api_response = GetMultiResponse(users,
                                        total=iteration_result.total,
                                        params=params,
                                        url=request.url,
                                        model=UserModel.MODEL,
                                        body=request.method == 'HEAD')
    except ManagerIterationError:
        #TODO: ERROR-FIX
        return abort(400)
    except ManagerGetError:
        #TODO: ERROR-FIX
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
    user_manager: UserManager = ManagerProvider.get_manager(ManagerType.USER_MANAGER, request_user)

    try:
        user: UserModel = user_manager.get(public_id)
    except ManagerGetError:
        return abort(404)

    api_response = GetSingleResponse(UserModel.to_dict(user),
                                     url=request.url,
                                     model=UserModel.MODEL,
                                     body=request.method == 'HEAD')

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
    user_manager: UserManager = ManagerProvider.get_manager(ManagerType.USER_MANAGER, request_user)

    try:
        user = UserModel.from_data(data=data)
        user_manager.update(public_id=PublicID(public_id), user=user)

        api_response = UpdateSingleResponse(result=UserModel.to_dict(user), url=request.url, model=UserModel.MODEL)
    except ManagerGetError:
        #TODO: ERROR-FIX
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
    user_manager: UserManager = ManagerProvider.get_manager(ManagerType.USER_MANAGER, request_user)
    security_manager: SecurityManager = ManagerProvider.get_manager(ManagerType.SECURITY_MANAGER, request_user)

    try:
        user = user_manager.get(public_id=public_id)
        password = security_manager.generate_hmac(request.json.get('password'))
        user.password = password
        user_manager.update(PublicID(public_id), user)
        api_response = UpdateSingleResponse(result=UserModel.to_dict(user), url=request.url, model=UserModel.MODEL)
    except ManagerGetError:
        #TODO: ERROR-FIX
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
    user_manager: UserManager = ManagerProvider.get_manager(ManagerType.USER_MANAGER, request_user)

    try:
        deleted_group = user_manager.delete(public_id=PublicID(public_id))
        api_response = DeleteSingleResponse(raw=UserModel.to_dict(deleted_group), model=UserModel.MODEL)
    except ManagerGetError as err:
        #TODO: ERROR-FIX
        LOGGER.debug("[delete_user] ManagerGetError: %s", err.message)
        return abort(404, f"Could not delete user with ID: {public_id} !")
    except ManagerDeleteError as err:
        #TODO: ERROR-FIX
        LOGGER.debug("[delete_user] ManagerDeleteError: %s", err.message)
        return abort(404, f"Could not delete user with ID: {public_id} !")

    return api_response.make_response()
