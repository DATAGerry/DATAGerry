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
from typing import List
from flask import make_response as flask_response
from werkzeug.wrappers import BaseResponse

from cmdb.framework.utils import PublicID
from cmdb.interface import DEFAULT_MIME_TYPE


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
    __slots__ = 'operation_type', 'time'

    def __init__(self, operation_type: OperationType):
        if operation_type.value not in set(item.value for item in OperationType):
            raise TypeError(f'{operation_type} is not a valid response operation')
        self.operation_type: OperationType = operation_type
        self.time: str = datetime.now().isoformat()

    def make_response(self, *args, **kwargs) -> BaseResponse:
        """Abstract method for http response
        Returns:
            http BaseResponse
        """
        raise NotImplementedError

    def export(self, text: str = 'json') -> dict:
        return {
            'response_type': self.operation_type.value,
            'time': self.time
        }


class GetSingleResponse(BaseAPIResponse):
    __slots__ = 'result'

    def __init__(self, result: dict):
        self.result: dict = result
        super(GetSingleResponse, self).__init__(operation_type=OperationType.GET)

    def make_response(self) -> BaseResponse:
        return make_api_response(self.export())

    def export(self, text: str = 'json') -> dict:
        return {**{
            'result': self.result
        }, **super(GetSingleResponse, self).export()}


class InsertSingleResponse(BaseAPIResponse):
    __slots__ = 'result_id'

    def __init__(self, result_id: PublicID):
        self.result_id = result_id
        super(InsertSingleResponse, self).__init__(operation_type=OperationType.INSERT)

    def make_response(self, prefix) -> BaseResponse:
        response = make_api_response(self.export(), 201)
        response.headers['location'] = f'{prefix}/{self.result_id}'
        return response

    def export(self, text: str = 'json') -> dict:
        return {**{
            'result_id': self.result_id
        }, **super(InsertSingleResponse, self).export()}


class GetMultiResponse(BaseAPIResponse):
    __slots__ = 'results', 'count', 'total'

    def __init__(self, results: List[dict], total: int):
        self.results: List[dict] = results
        self.count: int = len(self.results)
        self.total: int = total
        super(GetMultiResponse, self).__init__(operation_type=OperationType.GET)

    def make_response(self) -> BaseResponse:
        return make_api_response(self.export())

    def export(self, text: str = 'json') -> dict:
        return {**{
            'results': self.results,
            'count': self.count,
            'total': self.total
        }, **super(GetMultiResponse, self).export()}
