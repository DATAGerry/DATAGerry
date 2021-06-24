# DATAGERRY - OpenSource Enterprise CMDB
# Copyright (C) 2019 - 2021 NETHINKS GmbH
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


from json import dumps
from datetime import datetime, timezone
from enum import Enum
from math import ceil
from typing import List
from flask import make_response as flask_response
from werkzeug.wrappers import BaseResponse

from cmdb.framework.utils import PublicID, Model
from cmdb.interface import DEFAULT_MIME_TYPE
from cmdb.interface.api_parameters import CollectionParameters, APIParameters
from cmdb.interface.api_project import APIProjection, APIProjector

from cmdb.interface.api_pagination import APIPagination, APIPager
from cmdb.interface.route_utils import default


def make_api_response(body, status: int = 200, mime: str = None, indent: int = 2) -> BaseResponse:
    """
    Make a valid http response.

    Args:
        body: http body content
        status: http status code
        mime: mime type
        indent: display indent

    Returns:
        BaseResponse
    """
    from cmdb.interface import API_VERSION

    response = flask_response(dumps(body, default=default, indent=indent), status)
    response.mimetype = mime or DEFAULT_MIME_TYPE
    response.headers['X-API-Version'] = API_VERSION
    return response


class OperationType(Enum):
    """
    Enum for different response operations.
    Works as identifier beside the class instance.
    """
    GET = 'GET'
    UPDATE = 'UPDATE'
    PATCH = 'PATCH'
    INSERT = 'INSERT'
    DELETE = 'DELETE'


class ResponseMessage:
    """Simple class wrapper for json encoding"""

    def __init__(self, obj: dict = None):
        self.obj = obj


class ResponseSuccessMessage(ResponseMessage):
    """Message wrapper for successfully objects"""

    def __init__(self, public_id: int, status: int, obj: dict = None):
        """Init message
        Args:
            status: the given status code
            public_id: ID of the new object
            obj (optional): cmdb object instance
        """
        self.status = status
        self.public_id = public_id
        super(ResponseSuccessMessage, self).__init__(obj=obj)


class ResponseFailedMessage(ResponseMessage):
    """Message wrapper for failed objects"""

    def __init__(self, error_message: str, status: int, public_id: int = None, obj: dict = None):
        """Init message
        Args:
            status: the given status code of exceptions
            error_message: reason why it failed - exception error or something
            public_id (optional): failed public_id
            obj (optional): failed dict
        """
        self.status = status
        self.public_id = public_id
        self.error_message = error_message
        super(ResponseFailedMessage, self).__init__(obj=obj)

    def to_dict(self) -> dict:
        return {
            'status': self.status,
            'public_id': self.public_id,
            'error_message': self.error_message,
            'obj': self.obj,
        }


class BaseAPIResponse:
    """Basic `abstract` response class"""
    __slots__ = 'url', 'operation_type', 'time', 'model', 'body'

    def __init__(self, operation_type: OperationType, url: str = None, model: Model = None, body: bool = None):
        """
        Constructor of a basic api response.

        Args:
            operation_type:
            url:
            model:
            body
        """
        if operation_type.value not in set(item.value for item in OperationType):
            raise TypeError(f'{operation_type} is not a valid response operation')
        self.operation_type: OperationType = operation_type
        self.url = url or ''
        self.model: Model = model or ''
        self.body = body or True
        self.time: str = datetime.now(timezone.utc).isoformat()

    def make_response(self, *args, **kwargs) -> BaseResponse:
        """
        Abstract method for http response

        Returns:
            http BaseResponse
        """
        raise NotImplementedError

    def export(self, text: str = 'json') -> dict:
        """
        Get the raw information about this response.

        Args:
            text: return type - not used at the moment

        Returns:
            raw data information
        """
        return {
            'response_type': self.operation_type.value,
            'model': self.model,
            'time': self.time
        }


class GetSingleResponse(BaseAPIResponse):
    """
    API Response for get calls with a single resource.
    """
    __slots__ = 'result'

    def __init__(self, result: dict, url: str = None, model: Model = None, body: bool = None, projection: dict = None):
        """
        Constructor of GetSingleResponse.

        Args:
            result: body payload
            url: requested url
            model: model type of body
        """
        if projection:
            projection = APIProjection(projection)
            self.result = APIProjector(result, projection).project
        else:
            self.result: dict = result
        super(GetSingleResponse, self).__init__(operation_type=OperationType.GET, url=url, model=model,
                                                body=body)

    def make_response(self, *args, **kwargs) -> BaseResponse:
        """
        Make a valid http response.

        Args:
            *args:
            **kwargs:

        Returns:
            Instance of BaseResponse with a HTTP 200 status code.
        """
        if self.body:
            response = make_api_response(self.export(*args, **kwargs))
        else:
            response = make_api_response(None)
        return response

    def export(self, text: str = 'json') -> dict:
        """Get content of the response as dict."""
        return {**{
            'result': self.result
        }, **super(GetSingleResponse, self).export()}


class GetMultiResponse(BaseAPIResponse):
    """
    API Response for get calls with a collection of resources.
    """
    __slots__ = 'results', 'count', 'total', 'parameters', 'pager', 'pagination'

    def __init__(self, results: List[dict], total: int, params: CollectionParameters, url: str = None,
                 model: Model = None, body: bool = None):
        """
        Constructor of GetMultiResponse.

        Args:
            results: List of filtered elements in payload.
            total: Complete number of elements.
            params: HTTP query parameters.
            url: Requested url.
            model: Data-Model of the results.
            body: If http response should not have a body.

        """
        self.parameters = params
        if self.parameters.projection:
            project = APIProjection(self.parameters.projection)
            self.results = APIProjector(results, project).project
        else:
            self.results = results
        self.count: int = len(self.results)
        self.total: int = total

        if params.limit == 0:
            total_pages = 1
        else:
            total_pages = ceil(total / params.limit)
        self.pager: APIPager = APIPager(page=params.page, page_size=params.limit,
                                        total_pages=total_pages)
        self.pagination: APIPagination = APIPagination.create(url, self.pager.page, self.pager.total_pages)
        super(GetMultiResponse, self).__init__(operation_type=OperationType.GET, url=url, model=model,
                                               body=body)

    def make_response(self, *args, **kwargs) -> BaseResponse:
        """
        Make a valid http response.

        Args:
            *args:
            **kwargs:

        Returns:
            Instance of BaseResponse.
        """
        if self.body:
            response = make_api_response(self.export(*args, **kwargs))
        else:
            response = make_api_response(None)
        response.headers['X-Total-Count'] = self.total
        return response

    def export(self, text: str = 'json', pagination: bool = True) -> dict:
        """
        Get the response data as dict.

        Args:
            text: Currently optional data wrapper.
            pagination: Should the response include pagination data.

        Returns:
            Instance as a dict.

        """
        extra = {}
        if pagination:
            extra = {
                'parameters': CollectionParameters.to_dict(self.parameters),
                'pager': self.pager.to_dict(),
                'pagination': self.pagination.to_dict()
            }
        return {**{
            'results': self.results,
            'count': self.count,
            'total': self.total,
            **extra
        }, **super(GetMultiResponse, self).export()}


class InsertSingleResponse(BaseAPIResponse):
    """
    API Response for insert call of a single resource.
    """
    __slots__ = 'result_id', 'raw'

    def __init__(self, raw: dict, result_id: [PublicID, str] = None, url: str = None, model: Model = None):
        """
        Constructor of InsertSingleResponse.

        Args:
            result_id: The new public id or a identifier of the inserted resource.
            raw: The raw document
            url: The request url.
            model: Data model of the inserted resource.
        """

        self.raw: dict = raw
        self.result_id: PublicID = result_id
        super(InsertSingleResponse, self).__init__(operation_type=OperationType.INSERT, url=url, model=model)

    def make_response(self, prefix: str = '', *args, **kwargs) -> BaseResponse:
        """
        Make a vaid http response.

        Args:
            prefix: URL route prefix for header location settings.
            *args:
            **kwargs:

        Returns:
            Instance of BaseResponse with http status code 201.
        """
        response = make_api_response(self.export(), 201)
        response.headers['Location'] = f'{self.url}{self.result_id}'
        return response

    def export(self, text: str = 'json', *args, **kwargs) -> dict:
        """Get the data response payload as dict"""
        return {**{
            'result_id': self.result_id,
            'raw': self.raw
        }, **super(InsertSingleResponse, self).export(*args, **kwargs)}


class UpdateSingleResponse(BaseAPIResponse):
    """
    API Response for update call of a single resource.
    """

    __slots__ = 'result', 'failed'

    def __init__(self, result: dict, failed: ResponseFailedMessage = None, url: str = None, model: Model = None):
        """
        Constructor of UpdateSingleResponse.

        Args:
            result: Updated resource.
            failed: Failed data update
            url: Requested url.
            model: Data model of updated resource.
        """
        self.result: dict = result
        self.failed: ResponseFailedMessage = failed
        super(UpdateSingleResponse, self).__init__(operation_type=OperationType.UPDATE, url=url, model=model)

    def make_response(self, *args, **kwargs) -> BaseResponse:
        """
        Make a valid http response.

        Args:
            *args:
            **kwargs:

        Returns:
            Instance of BaseResponse with http status code 202
        """
        response = make_api_response(self.export(), 202)
        response.headers['Location'] = f'{self.url}'
        return response

    def export(self, text: str = 'json', *args, **kwargs) -> dict:
        """
        Get the update instance as dict.
        """
        return {**{
            'result': self.result,
            'failed': self.failed.to_dict(),
        }, **super(UpdateSingleResponse, self).export(*args, **kwargs)}


class UpdateMultiResponse(BaseAPIResponse):
    """
    API Response for update call of a multiple resources.
    """

    __slots__ = 'results', 'failed'

    def __init__(self, results: List[dict], failed: List[ResponseFailedMessage] = None,
                 url: str = None, model: Model = None):
        """
        Constructor of UpdateSingleResponse.

        Args:
            results: Updated resources.
            failed: Failed data update
            url: Requested url.
            model: Data model of updated resource.
        """
        self.results: List[dict] = results
        self.failed: List[ResponseFailedMessage] = failed or []
        super(UpdateMultiResponse, self).__init__(operation_type=OperationType.UPDATE, url=url, model=model)

    def make_response(self, *args, **kwargs) -> BaseResponse:
        """
        Make a valid http response.

        Args:
            *args:
            **kwargs:

        Returns:
            Instance of BaseResponse with http status code 202
        """
        response = make_api_response(self.export(), 202)
        return response

    def export(self, text: str = 'json', *args, **kwargs) -> dict:
        """
        Get the update instance as dict.
        """
        return {**{
            'results': self.results,
            'failed': self.failed,
        }, **super(UpdateMultiResponse, self).export(*args, **kwargs)}


class DeleteSingleResponse(BaseAPIResponse):
    """
    API Response for delete call of a single resource.
    """
    __slots__ = 'raw'

    def __init__(self, raw: dict = None, url: str = None, model: Model = None):
        """
        Constructor of DeleteSingleResponse.

        Args:
            raw: Content of deleted resource.
            url: Requested url.
            model: Data model of deleted resource.
        """
        self.raw = raw
        super(DeleteSingleResponse, self).__init__(operation_type=OperationType.DELETE, url=url, model=model)

    def make_response(self, *args, **kwargs) -> BaseResponse:
        """
        Make a valid http response.

        Args:
            *args:
            **kwargs:

        Returns:
            Instance of BaseResponse with 204 if raw content was set else 202
        """
        status_code = 204 if not self.raw else 202
        return make_api_response(self.export(*args, **kwargs), status_code)

    def export(self, text: str = 'json') -> dict:
        """
        Get the delete instance as dict.
        """
        return {**{
            'raw': self.raw
        }, **super(DeleteSingleResponse, self).export()}


class GetListResponse(BaseAPIResponse):
    """
    API Response for a simple list without iteration.
    """
    __slots__ = 'results', 'params'

    def __init__(self, results: List[dict], url: str = None, model: Model = None, body: bool = None,
                 params: APIParameters = None):

        self.params = params
        if self.params and self.params.projection:
            projection = APIProjection(self.params.projection)
            self.results = APIProjector(results, projection).project
        else:
            self.results: List[dict] = results
        super(GetListResponse, self).__init__(operation_type=OperationType.GET, url=url, model=model, body=body)

    def make_response(self, *args, **kwargs) -> BaseResponse:
        """
        Make a valid http response.

        Args:
            *args:
            **kwargs:

        Returns:
            Instance of BaseResponse with a HTTP 200 status code.
        """
        if self.body:
            response = make_api_response(self.export(*args, **kwargs))
        else:
            response = make_api_response(None)
        response.headers['X-Total-Count'] = len(self.results)
        return response

    def export(self, text: str = 'json') -> dict:
        """
        Get the list response
        """
        return {**{
            'results': self.results
        }, **super(GetListResponse, self).export()}
