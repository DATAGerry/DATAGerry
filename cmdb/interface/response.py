# DATAGERRY - OpenSource Enterprise CMDB
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
# along with this program. If not, see <https://www.gnu.org/licenses/>.
from json import dumps
from datetime import datetime
from enum import Enum
from math import ceil
from typing import List
from flask import make_response as flask_response
from werkzeug.wrappers import BaseResponse

from cmdb.framework.utils import PublicID, Model
from cmdb.interface import DEFAULT_MIME_TYPE
from cmdb.interface.api_parameters import CollectionParameters

from cmdb.interface.pagination import APIPagination, APIPager
from cmdb.utils import json_encoding


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

    response = flask_response(dumps(body, default=json_encoding.default, indent=indent), status)
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
        self.time: str = datetime.now().isoformat()

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

    def __init__(self, result: dict, url: str = None, model: Model = None, body: bool = None):
        """
        Constructor of GetSingleResponse.

        Args:
            result: body payload
            url: requested url
            model: model type of body
        """
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
            body_less: If http response should not have a body.

        """
        self.results: List[dict] = results
        self.count: int = len(self.results)
        self.total: int = total
        self.parameters = params
        self.pager: APIPager = APIPager(page=params.page, page_size=params.limit,
                                        total_pages=ceil(total / params.limit))
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
                'parameters': self.parameters.to_dict(),
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

    def __init__(self, result_id: PublicID, raw: dict, url: str = None, model: Model = None):
        """
        Constructor of InsertSingleResponse.

        Args:
            result_id: The new public id of the inserted resource.
            raw: The raw document
            url: The request url.
            model: Data model of the inserted resource.
        """
        self.result_id: PublicID = result_id
        self.raw: dict = raw
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
        response.headers['location'] = f'{self.url}/{self.result_id}'
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

    __slots__ = 'result'

    def __init__(self, result: dict, url: str = None, model: Model = None):
        """
        Constructor of UpdateSingleResponse.

        Args:
            result: Updated resource.
            url: Requested url.
            model: Data model of updated resource.
        """
        self.result: dict = result
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
        return response

    def export(self, text: str = 'json', *args, **kwargs) -> dict:
        """
        Get the update instance as dict.
        """
        return {**{
            'result': self.result
        }, **super(UpdateSingleResponse, self).export(*args, **kwargs)}


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
            'deleted_entry': self.raw
        }, **super(DeleteSingleResponse, self).export()}
