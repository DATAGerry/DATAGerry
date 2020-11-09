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
import { TableState, TableStatePayload } from './table.types';
import { Observable, ReplaySubject } from 'rxjs';
import { UserSetting } from '../../management/user-settings/models/user-setting';
import { map } from 'rxjs/operators';
import { convertResourceURL } from '../../management/user-settings/services/user-settings.service';

@Injectable({
  providedIn: 'root'
})
export class TableService<C = TableState> implements OnDestroy {

  /**
   * Component un-subscriber.
   * @private
   */
  private subscriber: ReplaySubject<void> = new ReplaySubject<void>();

  constructor(private indexDB: UserSettingsDBService<UserSetting, TableStatePayload>) {
  }

  /**
   * Get the table state payload from a user setting.
   * @param url
   * @param id
   */
  public getTableStatePayload(url: string, id: string): Observable<TableStatePayload> {
    return this.indexDB.getSetting(url).pipe(
      map((setting: UserSetting<TableStatePayload>) => {
        return setting.payloads.find(payload => payload.id === id);
      })
    );
  }

  /**
   * Get all states from a user setting.
   * @param url
   * @param id
   */
  public getTableStates(url: string, id: string): Observable<Array<TableState>> {
    return this.indexDB.getSetting(url).pipe(
      map((setting: UserSetting<TableStatePayload>) => {
        return setting.payloads.find(payload => payload.id === id).tableStates;
      })
    );
  }

  /**
   * Get a single state from a user setting by its name.
   * @param url
   * @param id
   * @param name
   */
  public getTableState(url: string, id: string, name: string): Observable<TableState> {
    return this.getTableStates(url, id).pipe(map((states: Array<TableState>) => {
      return states.find(state => state.name === name);
    }));
  }

  /**
   * Add a table state to a user setting.
   * @param url
   * @param id
   * @param state
   */
  public addTableState(url: string, id: string, state: TableState) {
    const resource: string = convertResourceURL(url);
    this.indexDB.getSetting(resource).subscribe((setting: UserSetting<TableStatePayload>) => {
      setting.payloads.find(payload => payload.id === id).tableStates.push(state);
      this.indexDB.updateSetting(setting);
    });
  }

  /**
   * Remove a table state from the payload.
   * @param url
   * @param id
   * @param state
   */
  public removeTableState(url: string, id: string, state: TableState) {
    const resource: string = convertResourceURL(url);
    this.indexDB.getSetting(resource).subscribe((setting: UserSetting<TableStatePayload>) => {
      const states = setting.payloads.find(payload => payload.id === id).tableStates;
      const stateIdx = states.findIndex(s => s.name === state.name);
      if (stateIdx > -1) {
        states.splice(stateIdx, 1);
        this.indexDB.updateSetting(setting);
      }
    });
  }

  public ngOnDestroy(): void {
    this.subscriber.next();
    this.subscriber.complete();
  }

}
