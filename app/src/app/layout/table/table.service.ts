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
import { UserSettingsDBService } from '../../management/user-settings/services/user-settings-db.service';
import { TableConfig, TableConfigPayload } from './table.types';
import { Observable, ReplaySubject } from 'rxjs';
import { UserSetting } from '../../management/user-settings/models/user-setting';
import { map } from 'rxjs/operators';
import { convertResourceURL } from '../../management/user-settings/services/user-settings.service';

@Injectable({
  providedIn: 'root'
})
export class TableService<C = TableConfig> implements OnDestroy {

  /**
   * Component un-subscriber.
   * @private
   */
  private subscriber: ReplaySubject<void> = new ReplaySubject<void>();

  constructor(private indexDB: UserSettingsDBService<UserSetting, TableConfigPayload>) {
  }

  /**
   * Get the table payload from a user setting.
   * @param url
   * @param id
   */
  public getTableConfigPayload(url: string, id: string): Observable<TableConfigPayload> {
    return this.indexDB.getSetting(url).pipe(
      map((setting: UserSetting<TableConfigPayload>) => {
        return setting.payloads.find(payload => payload.id === id);
      })
    );
  }

  /**
   * Get all configs from a user setting.
   * @param url
   * @param id
   */
  public getTableConfigs(url: string, id: string): Observable<Array<TableConfig>> {
    return this.indexDB.getSetting(url).pipe(
      map((setting: UserSetting<TableConfigPayload>) => {
        return setting.payloads.find(payload => payload.id === id).tableConfigs;
      })
    );
  }

  /**
   * Get a single config from a user setting by its name.
   * @param url
   * @param id
   * @param name
   */
  public getTableConfig(url: string, id: string, name: string): Observable<TableConfig> {
    return this.getTableConfigs(url, id).pipe(map((configs: Array<TableConfig>) => {
      return configs.find(config => config.name === name);
    }));
  }

  /**
   * Add a table config to a user setting.
   * @param url
   * @param id
   * @param config
   */
  public addTableConfig(url: string, id: string, config: TableConfig) {
    const resource: string = convertResourceURL(url);
    this.indexDB.getSetting(resource).subscribe((setting: UserSetting<TableConfigPayload>) => {
      setting.payloads.find(payload => payload.id === id).tableConfigs.push(config);
      this.indexDB.updateSetting(setting);
    });

  }

  public ngOnDestroy(): void {
    this.subscriber.next();
    this.subscriber.complete();
  }

}
