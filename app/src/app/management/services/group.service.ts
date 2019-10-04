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
import { AuthService } from '../../auth/services/auth.service';
import { Group } from '../models/group';
import { CmdbStatus } from '../../framework/models/cmdb-status';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { User } from '../models/user';
import { HttpParams } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class GroupService<T = Group> implements ApiService {

  public servicePrefix: string = 'group';
  private groups: any[];

  constructor(private api: ApiCallService) {
    this.getGroupList().subscribe((groups: T[]) => {
      this.groups = groups;
    });
  }

  // Find calls
  public findGroup(publicID: number): Group {
    return this.groups.find(g => g.public_id === publicID);
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

  public deleteGroup(publicID: number, action: string = null): Observable<T> {
    const groupDeleteOptions: any = httpObserveOptions;
    groupDeleteOptions.params = new HttpParams().set('action', action);
    return this.api.callDelete<T>(`${ this.servicePrefix }/${ publicID }/`, groupDeleteOptions).pipe(
      map((apiResponse) => {
        return apiResponse.body;
      })
    );
  }

}
