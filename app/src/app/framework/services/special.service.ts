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
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { ApiCallService, ApiService, resp } from '../../services/api-call.service';
import { CmdbDao } from '../models/cmdb-dao';
import {HttpClient, HttpHeaders} from '@angular/common/http';

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
export class SpecialService<T = CmdbDao> implements ApiService {
  public servicePrefix: string = '/';

  constructor(private api: ApiCallService, private http: HttpClient) {
  }

  public getNewestObjects(): Observable<T[]> {
    return this.api.callGet<T[]>(`object/newest/`).pipe(
      map((apiResponse) => {
        return apiResponse.body;
      })
    );
  }

  public getLatestObjects(): Observable<T[]> {
    return this.api.callGet<T[]>(`object/latest/`).pipe(
      map((apiResponse) => {
        return apiResponse.body;
      })
    );
  }

  public getIntroStarter(): Observable<T[]> {
    httpObserveOptions[PARAMETER] = { onlyActiveObjCookie: this.api.readCookies(COOCKIENAME) };
    return this.api.callGet<T[]>(this.servicePrefix + '/special/intro', this.http, httpObserveOptions).pipe(
      map((apiResponse) => {
        return apiResponse.body;
      })
    );
  }
}
