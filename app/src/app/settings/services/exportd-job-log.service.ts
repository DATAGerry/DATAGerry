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
import {ApiCallService, ApiService} from '../../services/api-call.service';
import { ExportdJob } from '../models/exportd-job';
import { map } from 'rxjs/operators';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ExportdJobLogService <T = any> implements ApiService {

  public servicePrefix: string = 'exportdlog';

  constructor(private api: ApiCallService) {
  }

  public getLogList(): Observable<T> {
    return this.api.callGet<T>(`${this.servicePrefix}/`).pipe(
      map((apiResponse) => {
        return apiResponse.body;
      })
    );
  }

  // CRUD calls
  public getJobLogs(publicID: number) {
    return this.api.callGet<T>(`${this.servicePrefix}/job/${publicID}/`).pipe(
      map((apiResponse) => {
        if (apiResponse.status === 204) {
          return [];
        }
        return apiResponse.body;
      })
    );
  }

  public getLogsWithExistingObject() {
    return this.api.callGet<T>(`${this.servicePrefix}/job/exists/`).pipe(
      map((apiResponse) => {
        if (apiResponse.status === 204) {
          return [];
        }
        return apiResponse.body;
      })
    );
  }

  public getLogsWithNotExistingObject() {
    return this.api.callGet<T>(`${this.servicePrefix}/job/notexists/`).pipe(
      map((apiResponse) => {
        if (apiResponse.status === 204) {
          return [];
        }
        return apiResponse.body;
      })
    );
  }

  public getDeleteLogs() {
    return this.api.callGet<T>(`${this.servicePrefix}/job/deleted/`).pipe(
      map((apiResponse) => {
        if (apiResponse.status === 204) {
          return [];
        }
        return apiResponse.body;
      })
    );
  }

  public deleteLog(publicID: number) {
    return this.api.callDelete<boolean>(`${this.servicePrefix}/${publicID}/`).pipe(
      map((apiResponse) => {
        return apiResponse.body;
      })
    );
  }
}
