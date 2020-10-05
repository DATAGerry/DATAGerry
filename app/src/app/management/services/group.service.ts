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
import {
  ApiCallService,
  ApiService,
  httpObserveOptions
} from '../../services/api-call.service';
import { Group } from '../models/group';
import { Observable, timer } from 'rxjs';
import { catchError, map, switchMap } from 'rxjs/operators';
import { HttpParams, HttpResponse } from '@angular/common/http';
import { FormControl } from '@angular/forms';
import { CollectionParameters } from '../../services/models/api-parameter';
import {
  APIGetMultiResponse,
  APIGetSingleResponse,
  APIInsertSingleResponse,
  APIUpdateSingleResponse
} from '../../services/models/api-response';

export const checkGroupNameExistsValidator = (groupService: GroupService, time: number = 500) => {
  return (control: FormControl) => {
    return timer(time).pipe(switchMap(() => {
      return groupService.getGroupByName(control.value).pipe(
        map((response) => {
          if (response === null) {
            return null;
          } else {
            return { groupNameExists: true };
          }
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
export class GroupService<T = Group> implements ApiService {

  public servicePrefix: string = 'group';

  constructor(private api: ApiCallService) {
  }

  /**
   * Iterate over a the complete group collection.
   * @param params CollectionParameters for the iteration.
   */
  public getGroups(params: CollectionParameters = {
    filter: undefined, limit: 10, sort: 'public_id', order: 1, page: 1
  }): Observable<APIGetMultiResponse<T>> {
    const options = httpObserveOptions;
    let httpParams: HttpParams = new HttpParams();
    if (params.filter !== undefined) {
      httpParams = httpParams.set('filter', params.filter);
    }
    httpParams = httpParams.set('limit', params.limit.toString());
    httpParams = httpParams.set('sort', params.sort);
    httpParams = httpParams.set('order', params.order.toString());
    httpParams = httpParams.set('page', params.page.toString());
    options.params = httpParams;
    return this.api.callGet<Array<T>>(`${ this.servicePrefix }/`, options).pipe(
      map((apiResponse: HttpResponse<APIGetMultiResponse<T>>) => {
        return apiResponse.body;
      })
    );
  }

  /**
   * Get a single group by its public id.
   * @param publicID: ID of the Group.
   */
  public getGroup(publicID: number): Observable<T> {
    return this.api.callGet<T>(this.servicePrefix + '/' + publicID).pipe(
      map((apiResponse: HttpResponse<APIGetSingleResponse<T>>) => {
        return apiResponse.body.result as T;
      })
    );
  }

  /**
   * Get a group by its name.
   * @param name: Name property of the selected group.
   */
  public getGroupByName(name: string): Observable<T> {
    const options = httpObserveOptions;
    const filter = { name };
    let params: HttpParams = new HttpParams();
    params = params.set('filter', JSON.stringify(filter));
    options.params = params;
    return this.api.callGet<Array<T>>(`${ this.servicePrefix }`, options).pipe(
      map((apiResponse: HttpResponse<APIGetMultiResponse<T>>) => {
        if (apiResponse.body.count === 0) {
          return null;
        }
        return apiResponse.body.results[0] as T;
      })
    );
  }

  /**
   * Insert a new group.
   * @param group: Data of the group.
   */
  public postGroup(group: T): Observable<T> {
    return this.api.callPost<T>(`${ this.servicePrefix }/`, group).pipe(
      map((apiResponse: HttpResponse<APIInsertSingleResponse<T>>) => {
        return apiResponse.body.raw as T;
      })
    );
  }

  /**
   * Update a existing group.
   * @param publicID ID of the selected group.
   * @param group Data of the new group.
   */
  public putGroup(publicID: number, group: T): Observable<T> {
    return this.api.callPut<T>(`${ this.servicePrefix }/${ publicID }/`, group).pipe(
      map((apiResponse: HttpResponse<APIUpdateSingleResponse<T>>) => {
        return apiResponse.body.result as T;
      })
    );
  }

  public deleteGroup(publicID: number, action: string = null, options: any = {}): Observable<T> {
    const groupDeleteOptions: any = httpObserveOptions;
    let params = new HttpParams();
    params = params.append('action', action);
    params = params.append('options', JSON.stringify(options));
    groupDeleteOptions.params = params;

    return this.api.callDelete<T>(`${ this.servicePrefix }/${ publicID }/`, groupDeleteOptions).pipe(
      map((apiResponse) => {
        return apiResponse.body;
      })
    );
  }

  // Special functions
  public checkGroupExists(groupName: string) {
    return this.api.callGet<T>(`${ this.servicePrefix }/${ groupName }`);
  }

}
