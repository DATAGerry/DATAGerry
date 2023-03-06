/*
* DATAGERRY - OpenSource Enterprise CMDB
* Copyright (C) 2023 becon GmbH
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
* along with this program. If not, see <https://www.gnu.org/licenses/>.
*/


import { Injectable } from '@angular/core';
import { ApiCallService, ApiService, httpObserveOptions, resp } from '../../services/api-call.service';
import { ExportdJob } from '../models/exportd-job';
import { map } from 'rxjs/operators';
import { Observable } from 'rxjs';
import { CollectionParameters } from '../../services/models/api-parameter';
import { APIGetMultiResponse } from '../../services/models/api-response';
import { HttpHeaders, HttpParams, HttpResponse } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class ExportdJobLogService<T = any> implements ApiService {

  public servicePrefix: string = 'exportdlog';
  public newServicePrefix: string = 'exportd/logs';

  public readonly options = {
    headers: new HttpHeaders({
      'Content-Type': 'application/json'
    }),
    params: {},
    observe: resp
  };

  constructor(private api: ApiCallService) {
  }

  /**
   * Iterate over the exportd logs collection
   * @param params Instance of CollectionParameters
   */
  public getLogs(params: CollectionParameters = {
    filter: undefined,
    limit: 10,
    sort: 'public_id',
    order: 1,
    page: 1
  }): Observable<APIGetMultiResponse<T>> {
    const options = httpObserveOptions;
    let httpParams: HttpParams = new HttpParams();
    if (params.filter !== undefined) {
      const filter = JSON.stringify(params.filter);
      httpParams = httpParams.set('filter', filter);
    }
    httpParams = httpParams.set('limit', params.limit.toString());
    httpParams = httpParams.set('sort', params.sort);
    httpParams = httpParams.set('order', params.order.toString());
    httpParams = httpParams.set('page', params.page.toString());
    options.params = httpParams;
    return this.api.callGet<Array<T>>(this.newServicePrefix, options).pipe(
      map((apiResponse: HttpResponse<APIGetMultiResponse<T>>) => {
        return apiResponse.body;
      })
    );
  }

  public getLogsWithExistingJobs(params: CollectionParameters = {
    filter: undefined,
    limit: 10,
    sort: 'public_id',
    order: 1,
    page: 1
  }): Observable<APIGetMultiResponse<T>> {
    const query = [
      { $match: { log_type: 'ExportdJobLog' } },
      { $match: { action: { $ne: 3 } } },
      { $lookup: { from: 'exportd.jobs', localField: 'job_id', foreignField: 'public_id', as: 'job' } },
      { $match: { job: { $ne: { $size: 0 } } } },
      { $project: { job: 0 } }
      ];
    if (params.filter !== undefined) {
      query.push(params.filter);
    }
    params.filter = query;
    return this.getLogs(params);
  }

  public getLogsWithNotExistingJobs(params: CollectionParameters = {
    filter: undefined,
    limit: 10,
    sort: 'public_id',
    order: 1,
    page: 1
  }): Observable<APIGetMultiResponse<T>> {
    const query = [
      { $match: { log_type: 'ExportdJobLog' } },
      { $match: { action: { $ne: 3 } } },
      { $lookup: { from: 'exportd.jobs', localField: 'job_id', foreignField: 'public_id', as: 'job' } },
      { $match: { job: { $size: 0 } } },
      { $project: { job: 0 } }
      ];

    if (params.filter !== undefined) {
      query.push(params.filter);
    }
    params.filter = query;
    return this.getLogs(params);
  }

  public getDeleteLogs() {
    const options = this.options;
    options.params = new HttpParams();
    return this.api.callGet<T>(`${ this.servicePrefix }/job/deleted/`, options).pipe(
      map((apiResponse) => {
        if (apiResponse.status === 204) {
          return [];
        }
        return apiResponse.body;
      })
    );
  }

  public deleteLog(publicID: number) {
    const options = this.options;
    options.params = new HttpParams();
    return this.api.callDelete<boolean>(`${ this.servicePrefix }/${ publicID }/`, options).pipe(
      map((apiResponse) => {
        return apiResponse.body;
      })
    );
  }
}
