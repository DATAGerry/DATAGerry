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
import { ActivatedRouteSnapshot, Resolve, RouterStateSnapshot } from '@angular/router';
import { UserSetting } from '../models/user-setting';
import { Observable } from 'rxjs';
import { UserSettingsDbService } from '../services/user-settings-db.service';
import { catchError, map } from 'rxjs/operators';
import { HttpResponse } from '@angular/common/http';
import { APIGetMultiResponse } from '../../../services/models/api-response';

/**
 * Resolver for the current user settings of a URL.
 */
@Injectable({
  providedIn: 'root'
})
export class UserSettingsResolver implements Resolve<UserSetting | unknown> {

  constructor(private userSettingsDB: UserSettingsDbService<UserSetting>) {
  }

  /**
   * Resolves data from the indexedDB by the current state URL.
   * @param route ActivatedRouteSnapshot
   * @param state RouterStateSnapshot
   */
  public resolve(route: ActivatedRouteSnapshot, state: RouterStateSnapshot):
    Observable<UserSetting | unknown> | Promise<UserSetting | unknown> | UserSetting | unknown {
    const currentURL = state.url;
    return this.userSettingsDB.getSetting(currentURL).pipe(
      map((setting: UserSetting) => {
        return setting;
      }),
      catchError((error) => {
        console.error(`No user setting for the route: ${currentURL} | Error: ${error}`);
        return undefined;
      })
    );
  }
}
