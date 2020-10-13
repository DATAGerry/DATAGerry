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
import { UserSettingsService } from './user-settings.service';
import { NgxIndexedDBService } from 'ngx-indexed-db';
import { UserSetting } from '../models/user-setting';

@Injectable({
  providedIn: 'root'
})
export class UserSettingsDbService<T = UserSetting> {

  private readonly storeName: string = 'UserSettings';

  constructor(private dbService: NgxIndexedDBService<any>, private userSettingsService: UserSettingsService) {

  }

  public getSetting(key: string) {
    return this.dbService.getByKey(this.storeName, key);
  }

  public addSetting(setting: UserSetting) {
    this.dbService.add(this.storeName, {
      identifier: setting.identifier,
      user_id: setting.user_id,
      setting: setting.setting,
      setting_type: setting.setting_type,
      setting_time: setting.setting_time
    }).subscribe(key => {
      console.log(key);
    });
  }
}
