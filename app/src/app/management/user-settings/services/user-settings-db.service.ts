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
import { UserSetting, UserSettingPayload } from '../models/user-setting';
import { Observable, ReplaySubject, Subject } from 'rxjs';
import { takeUntil } from 'rxjs/operators';
import { User } from '../../models/user';

@Injectable({
  providedIn: 'root'
})
export class UserSettingsDBService<T = UserSetting, P = UserSettingPayload> implements OnDestroy {

  /**
   * Name of the store settings of the indexedDB `DATAGERRY`.
   */
  private readonly storeName: string = 'user-settings';

  /**
   * Subscriber subject. When active auto set to backend db.
   */
  private subscriber: ReplaySubject<void> = new ReplaySubject<void>();

  /**
   * The current login user.
   */
  private readonly currentUser: User;

  /**
   * Holder subject when new settings are in the database.
   */
  private newSettings: Subject<UserSetting> = new Subject<UserSetting>();

  constructor(private dbService: NgxIndexedDBService<UserSetting<P>>,
              private userSettingsService: UserSettingsService<UserSetting<P>>) {
    this.newSettings.asObservable().pipe(takeUntil(this.subscriber)).subscribe();
    this.currentUser = this.userSettingsService.currentUser;
  }

  /**
   * Syncs the indexedDB settings with database.
   * @param settings List of UserSettings from the database.
   */
  public async syncSettings(settings: Array<UserSetting<P>>) {
    this.dbService.clear(this.storeName);

    for (const setting of settings) {
      await this.dbService.add(this.storeName, setting);
    }
  }

  /**
   * Get a setting by it ident.
   * @param resource Identifier of the setting.
   */
  public getSetting(resource: string): Observable<UserSetting<P>> {
    return this.dbService.getByKey(this.storeName, resource);
  }

  /**
   * Add a setting to the database.
   * @param setting UserSetting data.
   */
  public addSetting(setting: UserSetting<P>): void {
    this.dbService.add(this.storeName, setting).subscribe(key => {
      this.userSettingsService.addUserSetting(setting).pipe(takeUntil(this.subscriber)).subscribe();
    });
  }

  /**
   * Update a existing user setting.
   * @param setting UserSetting data.
   */
  public updateSetting(setting: UserSetting<P>): void {
    this.dbService.update(this.storeName, setting).subscribe(key => {
      this.userSettingsService.updateUserSetting(setting.resource, setting).pipe(takeUntil(this.subscriber)).subscribe();
    });
  }

  /**
   * Delete a existing user setting.
   * @param id User key.
   */
  public deleteSetting(id: string): void {
    this.dbService.delete(this.storeName, id).subscribe(key => {
      this.userSettingsService.deleteUserSetting(id).pipe(takeUntil(this.subscriber)).subscribe();
    });
  }

  /**
   * Auto unsubscribe when service is destroyed.
   */
  public ngOnDestroy(): void {
    this.subscriber.next();
    this.subscriber.complete();
  }
}
