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
import { ApiCallService, ApiService, httpObserveOptions } from '../../services/api-call.service';
import { Group } from '../models/group';
import { Observable, timer } from 'rxjs';
import { catchError, map, switchMap } from 'rxjs/operators';
import { HttpParams } from '@angular/common/http';
import { FormControl } from '@angular/forms';

export const checkGroupExistsValidator = (groupService: GroupService, time: number = 500) => {
  return (control: FormControl) => {
    return timer(time).pipe(switchMap(() => {
      return groupService.checkGroupExists(control.value).pipe(
        map(() => {
          return { groupExists: true };
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

  // CRUD calls
  public getGroupList(): Observable<T[]> {
    return this.api.callGet<T[]>(`${ this.servicePrefix }/`).pipe(
      map((apiResponse) => {
        if (apiResponse.status === 204) {
          return [];
        }
        return apiResponse.body;
      })
    );
  }

  public getGroup(publicID: number): Observable<T> {
    return this.api.callGet<T>(`${ this.servicePrefix }/${ publicID }`).pipe(
      map((apiResponse) => {
        return apiResponse.body;
      })
    );
  }

  public postGroup(data: T): Observable<T> {
    return this.api.callPost<T>(`${ this.servicePrefix }/`, data).pipe(
      map((apiResponse) => {
        return apiResponse.body;
      })
    );
  }

  public putGroup(publicID: number, data: T): Observable<T> {
    return this.api.callPut<T>(`${ this.servicePrefix }/${ publicID }/`, data).pipe(
      map((apiResponse) => {
        return apiResponse.body;
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
