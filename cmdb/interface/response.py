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


def make_api_response(view, status: int = 200, mime: str = None) -> BaseResponse:
    response = flask_response(dumps(view), status)
    response.mimetype = mime or DEFAULT_MIME_TYPE
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
    __slots__ = 'url', 'operation_type', 'time', 'model'

    def __init__(self, operation_type: OperationType, url: str = None, model: Model = None):
        if operation_type.value not in set(item.value for item in OperationType):
            raise TypeError(f'{operation_type} is not a valid response operation')
        self.operation_type: OperationType = operation_type
        self.url = url or ''
        self.model: Model = model or ''
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
    __slots__ = 'result'

    def __init__(self, result: dict, url: str = None, model: Model = None):
        self.result: dict = result
        super(GetSingleResponse, self).__init__(operation_type=OperationType.GET, url=url, model=model)

    def make_response(self) -> BaseResponse:
        return make_api_response(self.export())

    def export(self, text: str = 'json') -> dict:
        return {**{
            'result': self.result
        }, **super(GetSingleResponse, self).export()}


class GetMultiResponse(BaseAPIResponse):
    __slots__ = 'results', 'count', 'total', 'parameters', 'pager', 'pagination'

    def __init__(self, results: List[dict], total: int, params: CollectionParameters, url: str = None,
                 model: Model = None):
        self.results: List[dict] = results
        self.count: int = len(self.results)
        self.total: int = total
        self.parameters = params
        self.pager: APIPager = APIPager(page=params.page, page_size=params.limit,
                                        total_pages=ceil(total / params.limit))
        self.pagination: APIPagination = APIPagination.create(url, self.pager.page, self.pager.total_pages)
        super(GetMultiResponse, self).__init__(operation_type=OperationType.GET, url=url, model=model)

    def make_response(self) -> BaseResponse:
        return make_api_response(self.export())

    def export(self, text: str = 'json') -> dict:
        return {**{
            'results': self.results,
            'count': self.count,
            'total': self.total,
            'parameters': self.parameters.to_dict(),
            'pager': self.pager.to_dict(),
            'pagination': self.pagination.to_dict()
        }, **super(GetMultiResponse, self).export()}


class InsertSingleResponse(BaseAPIResponse):
    __slots__ = 'result_id'

    def __init__(self, result_id: PublicID, url: str = None, model: Model = None):
        self.result_id: PublicID = result_id
        super(InsertSingleResponse, self).__init__(operation_type=OperationType.INSERT, url=url, model=model)

    def make_response(self, prefix: str = '') -> BaseResponse:
        response = make_api_response(self.export(), 201)
        response.headers['location'] = f'{self.url}/{self.result_id}'
        return response

    def export(self, text: str = 'json') -> dict:
        return {**{
            'result_id': self.result_id
        }, **super(InsertSingleResponse, self).export()}


class DeleteSingleResponse(BaseAPIResponse):
    __slots__ = 'raw'

    def __init__(self, raw: dict, url: str = None, model: Model = None):
        self.raw = raw
        super(DeleteSingleResponse, self).__init__(operation_type=OperationType.DELETE, url=url, model=model)

    def make_response(self) -> BaseResponse:
        return make_api_response(self.export(), 202)

    def export(self, text: str = 'json') -> dict:
        return {**{
            'deleted_entry': self.raw
        }, **super(DeleteSingleResponse, self).export()}
