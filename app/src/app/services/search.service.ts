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
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { map } from 'rxjs/operators';
import { HttpClient, HttpHeaders} from '@angular/common/http';
import { RenderResult } from '../framework/models/cmdb-render';
import { ApiCallService, ApiService, resp } from './api-call.service';
import { Observable } from 'rxjs';

export const httpObserveOptions = {
  headers: new HttpHeaders({
    'Content-Type': 'application/json'
  }),
  observe: resp
};

export const PARAMETER = 'params';
export const COOCKIENAME = 'onlyActiveObjCookie';

@Injectable({
  providedIn: 'root'
})

export class SearchService<T = RenderResult> implements ApiService {

  public servicePrefix: string = 'search';

  constructor(private api: ApiCallService, private http: HttpClient, private modalService: NgbModal) {
  }

  // Calls

  public getSearchresults(value: string, startx: number, lengthx: number, limit: number = 0, typeID?: any): Observable<T[]> {
    httpObserveOptions[PARAMETER] = { onlyActiveObjCookie: this.readCookies(COOCKIENAME) };
    httpObserveOptions[PARAMETER].start = startx;
    httpObserveOptions[PARAMETER].length = lengthx;
    httpObserveOptions[PARAMETER].limit = limit;
    httpObserveOptions[PARAMETER].value = value;
    httpObserveOptions[PARAMETER].type_id = typeID;
    return this.api.callGet<T[]>(`${this.servicePrefix}/${value}`, this.http, httpObserveOptions).pipe(
      map((apiResponse) => {
        if (apiResponse.status === 204) {
          return [];
        }
        return apiResponse.body;
      })
    );
  }

  // Count calls

  public countSearchResult(value: string, typeID?: any) {
    httpObserveOptions[PARAMETER] = { onlyActiveObjCookie: this.readCookies(COOCKIENAME) };
    httpObserveOptions[PARAMETER].value = value;
    httpObserveOptions[PARAMETER].type_id = typeID;
    return this.api.callGet<number>(this.servicePrefix + '/count/', this.http, httpObserveOptions).pipe(
      map((apiResponse) => {
        if (apiResponse.status === 204) {
          return [];
        }
        return apiResponse.body;
      })
    );
  }

  readCookies(name: string) {
    const result = new RegExp('(?:^|; )' + encodeURIComponent(name) + '=([^;]*)').exec(document.cookie);
    return result ? result[1] : 'true';
  }
}
