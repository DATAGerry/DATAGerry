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


import { Injectable, OnDestroy } from '@angular/core';
import { UserSettingsService } from './user-settings.service';
import { NgxIndexedDBService } from 'ngx-indexed-db';
import { UserSetting } from '../models/user-setting';
import { Observable, ReplaySubject, Subject } from 'rxjs';
import { ToastService } from '../../../layout/toast/toast.service';
import { takeUntil } from 'rxjs/operators';
import { User } from '../../models/user';

@Injectable({
  providedIn: 'root'
})
export class UserSettingsDBService<T = UserSetting> implements OnDestroy {

  /**
   * Name of the store settings of the indexedDB `DATAGERRY`.
   */
  private readonly storeName: string = 'UserSettings';

  /**
   * Subscriber subject. When active auto set to backend db.
   */
  private updater: ReplaySubject<void>;

  /**
   * Holder subject when new settings are in the database.
   */
  private newSettings: Subject<UserSetting>;

  constructor(private dbService: NgxIndexedDBService<UserSetting>, private userSettingsService: UserSettingsService) {
    this.updater = new ReplaySubject<void>();
    this.newSettings = new Subject<UserSetting>();
    this.newSettings.asObservable().pipe(takeUntil(this.updater)).subscribe(

    );
  }

  /**
   * Syncs the indexedDB settings with database.
   * @param settings List of UserSettings from the database.
   */
  public async syncSettings(settings: Array<UserSetting>) {
    this.dbService.clear(this.storeName);

    for (const setting of settings) {
      await this.dbService.add(this.storeName, setting);
    }
  }

  /**
   * Get a setting by it ident.
   * @param key Identifier of the setting.
   */
  public getSetting(key: string): Observable<UserSetting> {
    return this.dbService.getByKey(this.storeName, key);
  }

  /**
   * Add a setting to the database.
   * @param setting UserSetting data.
   */
  public addSetting(setting: UserSetting): void {
    this.dbService.add(this.storeName, setting).subscribe(key => {
      this.userSettingsService.addUserSetting(setting).subscribe();
    });
  }

  /**
   * Update a existing user setting.
   * @param setting UserSetting data.
   */
  public updateSetting(setting: UserSetting): void {
    this.dbService.update(this.storeName, setting).subscribe(key => {
      this.userSettingsService.updateUserSetting(setting.identifier, setting).subscribe();
    });
  }

  /**
   * Delete a existing user setting.
   * @param identifier User key.
   */
  public deleteSetting(identifier: string): void {
    this.dbService.delete(this.storeName, identifier).subscribe(key => {
      this.userSettingsService.deleteUserSetting(identifier).subscribe();
    });
  }

  /**
   * Auto unsubscribe when service is destroyed.
   */
  public ngOnDestroy(): void {
    this.updater.next();
    this.updater.complete();
  }
}
