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
import { User } from '../models/user';
import { AuthService } from '../../auth/services/auth.service';
import { switchMap, map, catchError } from 'rxjs/operators';
import { Observable, timer } from 'rxjs';
import { HttpBackend, HttpParams, HttpResponse } from '@angular/common/http';
import { FormControl } from '@angular/forms';
import { CollectionParameters } from '../../services/models/api-parameter';
import {
  APIGetMultiResponse,
  APIGetSingleResponse,
  APIInsertSingleResponse,
  APIUpdateSingleResponse
} from '../../services/models/api-response';

export const userExistsValidator = (userService: UserService, time: number = 500) => {
  return (control: FormControl) => {
    return timer(time).pipe(switchMap(() => {
      return userService.getUserByName(control.value).pipe(
        map((response) => {
          if (response === null) {
            return null;
          } else {
            return { userExists: true };
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
export class UserService<T = User> implements ApiService {

  public readonly servicePrefix: string = 'users';

  constructor(private api: ApiCallService, private backend: HttpBackend, private authService: AuthService) {
  }

  /**
   * Get the current login user.
   */
  public getCurrentUser(): User {
    return this.authService.currentUserValue;
  }

  /**
   * Iterate over the user collection
   * @param params Instance of CollectionParameters
   */
  public getUsers(params: CollectionParameters = {
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
    return this.api.callGet<Array<T>>(this.servicePrefix + '/', options).pipe(
      map((apiResponse: HttpResponse<APIGetMultiResponse<T>>) => {
        return apiResponse.body;
      })
    );
  }

  /**
   * Get a specific user by the id
   * @param publicID PublicID of the user
   */
  public getUser(publicID: number): Observable<T> {
    return this.api.callGet<T>(this.servicePrefix + '/' + publicID).pipe(
      map((apiResponse: HttpResponse<APIGetSingleResponse<T>>) => {
        return apiResponse.body.result as T;
      })
    );
  }

  /**
   * Get the number of all users.
   */
  public countUsers(filter?: any): Observable<number> {
    const options = httpObserveOptions;
    if (filter !== undefined) {
      let httpParams: HttpParams = new HttpParams();
      httpParams = httpParams.set('filter', JSON.stringify(filter));
      options.params = httpParams;
    }
    return this.api.callHead<T>(`${ this.servicePrefix }/`, options).pipe(
      map((apiResponse: HttpResponse<APIGetMultiResponse<T>>) => {
        return +apiResponse.headers.get('X-Total-Count');
      })
    );
  }

  /**
   * Get user by the user_name.
   * @param name: Username of the user.
   */
  public getUserByName(name: string): Observable<T> {
    const options = httpObserveOptions;
    const filter = { user_name: name };
    let params: HttpParams = new HttpParams();
    params = params.set('filter', JSON.stringify(filter));
    options.params = params;
    return this.api.callGet<Array<T>>(this.servicePrefix + '/', options).pipe(
      map((apiResponse: HttpResponse<APIGetMultiResponse<T>>) => {
        console.log(apiResponse);
        if (apiResponse.body.count === 0) {
          return null;
        }
        return apiResponse.body.results[0] as T;
      })
    );
  }

  public changeUserPassword(userID: number, newPassword: string) {
    return this.api.callPut<boolean>(this.servicePrefix + '/' + userID + '/passwd', { password: newPassword });
  }

  /**
   * Get all users in a group.
   * @param groupID: PublicID of the user group.
   */
  public getUsersByGroup(groupID: number): Observable<Array<T>> {
    return this.api.callGet<Array<T>>(`${ this.servicePrefix }/?filter={"group_id": ${ groupID }}`).pipe(
      map((apiResponse: HttpResponse<APIGetMultiResponse<T>>) => {
        return apiResponse.body.results as Array<T>;
      })
    );
  }

  /**
   * Insert a new user.
   * @param user: Data of the user.
   */
  public postUser(user: T): Observable<T> {
    return this.api.callPost<User>(`${ this.servicePrefix }/`, user).pipe(
      map((apiResponse: HttpResponse<APIInsertSingleResponse<T>>) => {
        return apiResponse.body.raw as T;
      })
    );
  }

  /**
   * Update a existing user.
   * @param publicID: The PublicID of the selected user.
   * @param user: User instance of the selected user.
   */
  public putUser(publicID: number, user: T): Observable<T> {
    return this.api.callPut<T>(`${ this.servicePrefix }/${ publicID }/`, user).pipe(
      map((apiResponse: HttpResponse<APIUpdateSingleResponse<T>>) => {
        return apiResponse.body.result as T;
      })
    );
  }

  /**
   * Delete a existing user.
   * @param publicID: The PublicID of the selected user.
   */
  public deleteUser(publicID: number): Observable<boolean> {
    return this.api.callDelete<boolean>(`${ this.servicePrefix }/${ publicID }/`).pipe(
      map((apiResponse) => {
        return apiResponse.body;
      })
    );
  }

}
