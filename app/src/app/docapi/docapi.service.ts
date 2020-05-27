/*
* DATAGERRY - OpenSource Enterprise CMDB
* Copyright (C) 2019 NETHINKS GmbH
*
* This program is free software: you can redistribute it and/or modify
* it under the terms of the GNU Affero General Public License as
* published by the Free Software Foundation, either version 3 of the
* License, or (at your option) any later version.
*
* This program is distributed in the hope that it will be useful,
* but WITHOUT ANY WARRANTY; without even the implied warranty of
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
* GNU Affero General Public License for more details.

* You should have received a copy of the GNU Affero General Public License
* along with this program.  If not, see <https://www.gnu.org/licenses/>.
*/

import { Injectable } from '@angular/core';

import { HttpInterceptorHandler, ApiCallService, ApiService } from '../services/api-call.service';
import { HttpBackend, HttpClient, HttpResponse } from '@angular/common/http';
import { switchMap, map, catchError } from 'rxjs/operators';
import { Observable, timer } from 'rxjs';
import { DocTemplate } from '../framework/models/cmdb-doctemplate';

const fileHttpOptions = {
  observe: 'response',
  responseType: 'blob'
};


@Injectable({
  providedIn: 'root'
})
export class DocapiService<T = DocTemplate> implements ApiService {

  public readonly servicePrefix: string = 'docapi';

  constructor(private api: ApiCallService, private backend: HttpBackend) {
  }

  getDocTemplateList() : Observable<T[]> {
    return this.api.callGet<T>(`${ this.servicePrefix }/template/`).pipe(
      map((apiResponse) => {
        if (apiResponse.status === 204) {
          return [];
        }
        return apiResponse.body;
      })
    );
  }


  getObjectDocTemplateList(typeId: number) : Observable<T[]> {
    const searchfilter = {
        template_type: 'OBJECT',
        template_parameters: { type: typeId }
    }
    return this.api.callGet<T>(`${ this.servicePrefix }/template/by/${JSON.stringify(searchfilter)}`).pipe(
      map((apiResponse) => {
        if (apiResponse.status === 204) {
          return [];
        }
        return apiResponse.body;
      })
    );
  }


  getRenderedObjectDoc(templateId: number, objectId: number) {
    return this.api.callGetRoute<any>(`${ this.servicePrefix }/template/${ templateId }/render/${ objectId }`, fileHttpOptions);
  }


}
