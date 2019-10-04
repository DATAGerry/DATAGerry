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
import { ApiCallService, ApiService } from '../../services/api-call.service';
import { User } from '../models/user';
import { Group } from '../models/group';
import { AuthService } from '../../auth/services/auth.service';
import { Right } from '../models/right';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { CmdbStatus } from '../../framework/models/cmdb-status';
import { HttpResponse } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class UserService<T = User> implements ApiService {

  public readonly servicePrefix: string = 'user';
  private userList: any[] = [];

  constructor(private api: ApiCallService, private authService: AuthService) {
    this.getUserList().subscribe((respUserList: T[]) => {
      this.userList = respUserList;
    });
  }

  public getCurrentUser(): User {
    return this.authService.currentUserValue;
  }

  public getUserList(): Observable<T[]> {
    return this.api.callGet<T>(`${ this.servicePrefix }/`).pipe(
      map((apiResponse) => {
        if (apiResponse.status === 204) {
          return [];
        }
        return apiResponse.body;
      })
    );
  }

  public changeUserPassword(userID: number, newPassword: string) {
    return this.api.callPutRoute<boolean>(this.servicePrefix + '/' + userID + '/passwd', { password: newPassword });
  }

  public getUser(publicID: number): Observable<T> {
    return this.api.callGet<T>(`${ this.servicePrefix }/${ publicID }`).pipe(
      map((apiResponse) => {
        return apiResponse.body;
      })
    );
  }

  // tslint:disable-next-line:no-shadowed-variable
  public findUser(publicID: number): User | T {
    return this.userList.find(user => user.public_id === publicID);
  }

  public getUserByGroup(publicID: number): Observable<T[]> {
    return this.api.callGet<T>(`${ this.servicePrefix }/group/${ publicID }`).pipe(
      map((apiResponse) => {
        if (apiResponse.status === 204) {
          return [];
        }
        return apiResponse.body;
      })
    );
  }

  // CRUD functions
  public postUser(data: User) {
    return this.api.callPost<User>(`${ this.servicePrefix }/`, data).pipe(
      map((apiResponse: HttpResponse<any>) => {
        if (apiResponse.status === 400) {
          console.error("test");
        }
        return apiResponse.body;
      })
    );
  }

}
