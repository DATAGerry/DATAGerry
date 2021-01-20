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
  httpObserveOptions
} from '../../services/api-call.service';
import { ExportdJob } from '../models/exportd-job';
import { Observable, timer} from 'rxjs';
import { FormControl } from '@angular/forms';
import { catchError, map, switchMap } from 'rxjs/operators';
import { HttpBackend, HttpClient, HttpParams, HttpResponse } from '@angular/common/http';
import { BasicAuthInterceptor } from '../../auth/interceptors/basic-auth.interceptor';
import { AuthService } from '../../auth/services/auth.service';
import { CollectionParameters } from '../../services/models/api-parameter';
import { APIGetMultiResponse } from '../../services/models/api-response';

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
  private taskList: ExportdJob[];

  constructor(private api: ApiCallService) {
    this.getTaskList().subscribe((list: ExportdJob[]) => {
      this.taskList = list;
    });
  }

  public findTask(publicID: number): ExportdJob {
    return this.taskList.find(task => task.public_id === publicID);
  }

  public getTask(publicID: number) {
    return this.api.callGet<ExportdJob>(this.servicePrefix + '/' + publicID).pipe(
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

  public getTaskList() {
    return this.api.callGet<ExportdJob[]>(this.servicePrefix + '/').pipe(
      map((apiResponse) => {
        if (apiResponse.status === 204) {
          return [];
        }
        return apiResponse.body;
      })
    );
  }

  // CRUD calls
  public postTask(taskInstance: ExportdJob): Observable<any> {
    return this.api.callPost<ExportdJob>(this.servicePrefix + '/', taskInstance);
  }

  public putTask( taskInstance: ExportdJob): Observable<any> {
    return this.api.callPut(this.servicePrefix + '/', taskInstance);
  }

  public deleteTask(publicID: number) {
    return this.api.callDelete<number>(this.servicePrefix + '/' + publicID);
  }

  public run_task(publicID: number) {
    return this.api.callGet<ExportdJob>(this.servicePrefix + '/manual/' + publicID).pipe(
      map((apiResponse) => {
        if (apiResponse.status === 204) {
          return [];
        }
        return apiResponse.body;
      })
    );
  }

  // Validation functions
  public checkJobExists(typeName: string) {
    return this.api.callGet<T>(`${ this.servicePrefix }/name/${ typeName }`);
  }
}
