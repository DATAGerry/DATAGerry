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
import { ProgressBarInstance } from './progress-bar/progress-bar.types';


@Injectable({
  providedIn: 'root'
})
export class ProgressBarService {

  /**
   * Instance map.
   * @private
   */
  private instances: { [id: string]: ProgressBarInstance } = {};

  /**
   * Get the progressbar instance from the map by its id.
   * @param id
   */
  public getInstance(id: string = 'default'): ProgressBarInstance {
    if (!this.instances[id]) {
      this.instances[id] = new ProgressBarInstance();
    }
    return this.instances[id];
  }

}
