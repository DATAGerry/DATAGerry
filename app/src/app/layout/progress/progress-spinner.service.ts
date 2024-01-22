/*
* DATAGERRY - OpenSource Enterprise CMDB
* Copyright (C) 2024 becon GmbH
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
import { BehaviorSubject, Observable } from 'rxjs';
import { ProgressSpinner } from './progress-spinner/progress-spinner.types';

@Injectable({
  providedIn: 'root'
})
export class ProgressSpinnerService {

  public static readonly DEFAULT_TEXT: string = 'Loading';

  /**
   * Instance map.
   * @private
   */
  private spinner: { [id: string]: BehaviorSubject<ProgressSpinner> } = {};

  /**
   * Get the progressbar instance from the map by its id.
   * @param id
   */
  private getSpinnerInstance(id: string = 'app'): BehaviorSubject<ProgressSpinner> {
    if (!this.spinner[id]) {
      this.spinner[id] = new BehaviorSubject<ProgressSpinner>({
        show: false,
        text: ProgressSpinnerService.DEFAULT_TEXT
      });
    }
    return this.spinner[id];
  }

  public getSpinner(id: string = 'app'): Observable<ProgressSpinner> {
    return this.getSpinnerInstance(id).asObservable();
  }

  public show(id: string = 'app', text?: string): void {
    this.getSpinnerInstance(id).next({ show: true, text });
  }

  public hide(id: string = 'app'): void {
    this.getSpinnerInstance(id).next({ show: false });
  }

}
