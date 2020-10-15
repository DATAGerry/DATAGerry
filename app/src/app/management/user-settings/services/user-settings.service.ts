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
* along with this program. If not, see <https://www.gnu.org/licenses/>.
*/

import { Injectable } from '@angular/core';
import { ApiCallService, ApiService } from '../../../services/api-call.service';
import { UserSetting } from '../models/user-setting';
import { AuthService } from '../../../auth/services/auth.service';
import { User } from '../../models/user';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { HttpResponse } from '@angular/common/http';
import {
  APIDeleteSingleResponse,
  APIGetListResponse, APIGetSingleResponse,
  APIInsertSingleResponse,
  APIUpdateSingleResponse
} from '../../../services/models/api-response';

/**
 * Service class for API user settings.
 */
@Injectable({
  providedIn: 'root'
})
export class UserSettingsService<T = UserSetting> implements ApiService {

  /**
   * Default REST URL Prefix.
   */
  public servicePrefix: string;

  /**
   * The current login user.
   */
  private currentUser: User;

  /**
   * Constructor of `UserSettingsService`.
   * Generates the servicePrefix as `users/{USER_ID}/settings`.
   *
   * @param api: ApiCallService
   * @param authService: AuthService
   */
  constructor(private api: ApiCallService, private authService: AuthService) {
    this.currentUser = this.authService.currentUserValue;
    if (this.currentUser) {
      this.servicePrefix = `users/${ this.currentUser.public_id }/settings`;
    }
  }

  /**
   * Get all settings from the logged user.
   */
  public getUserSettings(): Observable<Array<T>> {
    return this.api.callGet<T>(`${ this.servicePrefix }/`).pipe(
      map((apiResponse: HttpResponse<APIGetListResponse<T>>) => {
        return apiResponse.body.results as Array<T>;
      })
    );
  }

  /**
   * Get a specific setting from the logged user.
   * @param identifier of the setting.
   */
  public getUserSetting(identifier: string): Observable<T> {
    return this.api.callGet<T>(`${ this.servicePrefix }/${ identifier }/`).pipe(
      map((apiResponse: HttpResponse<APIGetSingleResponse<T>>) => {
        return apiResponse.body.result as T;
      })
    );
  }

  /**
   * Add a new setting for the logged in user.
   * @param setting data.
   */
  public addUserSetting(setting: T): Observable<T> {
    return this.api.callPost<T>(`${ this.servicePrefix }/`, setting).pipe(
      map((apiResponse: HttpResponse<APIInsertSingleResponse<T>>) => {
        return apiResponse.body.raw as T;
      })
    );
  }

  /**
   * Update a existing user setting by its identifier.
   * @param identifier of the setting.
   * @param setting data.
   */
  public updateUserSetting(identifier: string, setting: T): Observable<T> {
    return this.api.callPut<T>(`${ this.servicePrefix }/${ identifier }`, setting).pipe(
      map((apiResponse: HttpResponse<APIUpdateSingleResponse<T>>) => {
        return apiResponse.body.result as T;
      })
    );
  }

  /**
   * Delete a specific user setting by its identifier.
   * @param identifier of the setting.
   */
  public deleteUserSetting(identifier: string): Observable<T> {
    return this.api.callDelete<T>(`${ this.servicePrefix }/${ identifier }`).pipe(
      map((apiResponse: HttpResponse<APIDeleteSingleResponse<T>>) => {
        return apiResponse.body.deleted_entry as T;
      })
    );
  }

}
