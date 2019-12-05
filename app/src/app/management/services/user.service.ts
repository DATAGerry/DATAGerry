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
import { HttpInterceptorHandler, ApiCallService, ApiService } from '../../services/api-call.service';
import { User } from '../models/user';
import { AuthService } from '../../auth/services/auth.service';
import { switchMap, map, catchError } from 'rxjs/operators';
import { Observable, timer } from 'rxjs';
import { HttpBackend, HttpClient, HttpResponse } from '@angular/common/http';
import { FormControl } from '@angular/forms';
import { BasicAuthInterceptor } from '../../auth/interceptors/basic-auth.interceptor';

export const checkUserExistsValidator = (userService: UserService, time: number = 500) => {
  return (control: FormControl) => {
    return timer(time).pipe(switchMap(() => {
      return userService.checkUserExists(control.value).pipe(
        map(() => {
          return { userExists: true };
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
export class UserService<T = User> implements ApiService {

  public readonly servicePrefix: string = 'user';

  constructor(private api: ApiCallService, private backend: HttpBackend, private authService: AuthService) {
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
        return apiResponse.body;
      })
    );
  }

  public putUser(publicID: number, data: T): Observable<T> {
    return this.api.callPut<T>(`${ this.servicePrefix }/${ publicID }/`, data).pipe(
      map((apiResponse) => {
        return apiResponse.body;
      })
    );
  }

  public deleteUser(publicID: number): Observable<boolean> {
    return this.api.callDelete<boolean>(`${ this.servicePrefix }/${ publicID }/`).pipe(
      map((apiResponse) => {
        return apiResponse.body;
      })
    );
  }

  // Special functions
  public checkUserExists(userName: string) {
    const specialClient = new HttpClient(new HttpInterceptorHandler(this.backend, new BasicAuthInterceptor(this.authService)));
    return this.api.callGet<T>(`${ this.servicePrefix }/${ userName }`, specialClient);
  }
}
