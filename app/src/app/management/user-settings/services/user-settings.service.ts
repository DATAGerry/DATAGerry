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
import { NgxIndexedDBService } from 'ngx-indexed-db';
import { ApiCallService, ApiService } from '../../../services/api-call.service';
import { UserSetting } from '../models/user-setting';
import { AuthService } from '../../../auth/services/auth.service';
import { User } from '../../models/user';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { HttpResponse } from '@angular/common/http';
import { APIGetListResponse } from '../../../services/models/api-response';

@Injectable({
  providedIn: 'root'
})
export class UserSettingsService<T = UserSetting> implements ApiService {

  public servicePrefix: string;
  private readonly storeName: string = 'UserSettings';
  private currentUser: User;

  constructor(private api: ApiCallService, private authService: AuthService, private dbService: NgxIndexedDBService<T>) {
    this.currentUser = this.authService.currentUserValue;
    this.servicePrefix = `users/${ this.currentUser.public_id }/settings`;
  }

  public cleanUserSettings(): Observable<boolean> {
    return this.dbService.clear(this.storeName);
  }

  public getUserSettings(): Observable<Array<T>> {
    return this.api.callGet<T>(`${ this.servicePrefix }/`).pipe(
      map((apiResponse: HttpResponse<APIGetListResponse<T>>) => {
        return apiResponse.body.results as Array<T>;
      })
    );
  }

  public addUserSetting(setting: T): Observable<number> {
    return this.dbService.add(this.storeName, setting);
  }

  public updateUserSetting(setting: T): Observable<Array<T>> {
    return this.dbService.update(this.storeName, setting);
  }

  public deleteUserSetting(key: number): Observable<Array<T>> {
    return this.dbService.delete(this.storeName, key);
  }
}
