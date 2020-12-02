/*
* DATAGERRY - OpenSource Enterprise CMDB
* Copyright (C) 2019 - 2020 NETHINKS GmbH
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

import { BehaviorSubject, Observable } from 'rxjs';

export class ProgressBarInstance {

  public static readonly INIT_VALUE: number = 0;
  public static readonly MIN_VALUE: number = 0;
  public static readonly MAX_VALUE: number = 100;

  private _state: BehaviorSubject<ProgressBarState>;

  constructor() {
    this._state = new BehaviorSubject<ProgressBarState>({ value: 0 });
  }

  public get state(): Observable<ProgressBarState> {
    return this._state.asObservable();
  }

  public start() {
    this._state.next({ value: 10 });
  }

  public complete() {

  }

}

export interface ProgressBarState {
  value: number;
}
