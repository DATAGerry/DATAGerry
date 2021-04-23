/*
* DATAGERRY - OpenSource Enterprise CMDB
* Copyright (C) 2019 - 2021 NETHINKS GmbH
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
import {
  ApiCallService,
  ApiService,
  HttpInterceptorHandler,
  httpObserveOptions, resp
} from '../services/api-call.service';
import { ExportdJob } from '../settings/models/exportd-job';
import { Observable, timer} from 'rxjs';
import { FormControl } from '@angular/forms';
import { catchError, map, switchMap } from 'rxjs/operators';
import { HttpBackend, HttpClient, HttpHeaders, HttpParams, HttpResponse } from '@angular/common/http';
import { BasicAuthInterceptor } from '../auth/interceptors/basic-auth.interceptor';
import { AuthService } from '../auth/services/auth.service';
import { CollectionParameters } from '../services/models/api-parameter';
import { APIGetMultiResponse } from '../services/models/api-response';

export const checkJobExistsValidator = (jobService: ExportdJobService<ExportdJob>, time: number = 500) => {
  return (control: FormControl) => {
    return timer(time).pipe(switchMap(() => {
      return jobService.checkJobExists(control.value).pipe(
        map(() => {
          return { typeExists: true };
        }),
        catchError(() => {
          return new Promise(resolve => {
            resolve(null);
          });
        })
      );
    }));
  };
};

@Injectable({
  providedIn: 'root'
})
export class ExportdJobService<T = ExportdJob> implements ApiService {

  public servicePrefix: string = 'exportdjob';
  public newServicePrefix: string = 'exportd/jobs';

  public readonly options = {
    headers: new HttpHeaders({
      'Content-Type': 'application/json'
    }),
    params: {},
    observe: resp
  };

  constructor(private api: ApiCallService) {
  }

  public getTask(publicID: number) {
    const options = this.options;
    options.params = new HttpParams();
    return this.api.callGet<ExportdJob>(this.servicePrefix + '/' + publicID, options).pipe(
      map((apiResponse) => {
        if (apiResponse.status === 204) {
          return [];
        }
        return apiResponse.body;
      })
    );
  }

  /**
   * Iterate over the type collection
   * @param params Instance of CollectionParameters
   */
  public getTasks(params: CollectionParameters = {
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

  // CRUD calls
  public postTask(taskInstance: ExportdJob): Observable<T> {
    const options = this.options;
    options.params = new HttpParams();
    return this.api.callPost<ExportdJob>(this.servicePrefix + '/', taskInstance, options).pipe(
      map((apiResponse) => {
        return apiResponse.body;
      })
    );
  }

  public putTask( taskInstance: ExportdJob): Observable<any> {
    const options = this.options;
    options.params = new HttpParams();
    return this.api.callPut(this.servicePrefix + '/', taskInstance, options).pipe(
      map((apiResponse) => {
        return apiResponse.body;
      })
    );
  }

  public deleteTask(publicID: number): Observable<any> {
    const options = this.options;
    options.params = new HttpParams();
    return this.api.callDelete<number>(this.servicePrefix + '/' + publicID, options).pipe(
      map((apiResponse) => {
        return apiResponse.body;
      })
    );
  }

  public run_task(publicID: number): Observable<any> {
    const options = this.options;
    options.params = new HttpParams();
    return this.api.callGet<ExportdJob>(this.servicePrefix + '/manual/' + publicID, options).pipe(
      map((apiResponse) => {
        return apiResponse.body;
      })
    );
  }

  // Validation functions
  public checkJobExists(typeName: string) {
    const options = this.options;
    options.params = new HttpParams();
    return this.api.callGet<T>(`${ this.servicePrefix }/name/${ typeName }`, options);
  }
}
