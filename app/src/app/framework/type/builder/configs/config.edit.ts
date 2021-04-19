/*
* DATAGERRY - OpenSource Enterprise CMDB
* Copyright (C) 2019 - 2021 NETHINKS GmbH
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

import { Component, Input } from '@angular/core';
import { CmdbType } from '../../../models/cmdb-type';
import { CmdbMode } from '../../../modes.enum';
import { Group } from '../../../../management/models/group';
import { User } from '../../../../management/models/user';

@Component({
  template: ``
})
export class ConfigEditBaseComponent {

  /**
   * Cmdb modes for template usage.
   */
  public MODES = CmdbMode;

  /**
   *
   */
  @Input() public mode: CmdbMode = CmdbMode.Create;
  @Input() public data: any;


  @Input() public types: Array<CmdbType> = [];
  @Input() public groups: Array<Group> = [];
  @Input() public users: Array<User> = [];

  @Input() public sections: Array<any>;
  @Input() public fields: Array<any> = [];


  public constructor() {
  }

  public calculateName(value) {
    if (this.mode !== CmdbMode.Edit) {
      this.data.name = value.replace(/ /g, '-').toLowerCase();
      this.data.name = this.data.name.replace(/[^a-z0-9 \-]/gi, '').toLowerCase();
    }
    if (!this.checkNameUniqueness()) {
      this.calculateName(this.data.name += '-1');
    }
  }

  private checkNameUniqueness() {
    const { type, name } = this.data;
    switch (type) {
      case 'section':
        return this.sections.filter(el => el.name === name).length <= 1;
      default:
        let count = 0;
        this.sections.forEach((sec) => {
          count += sec.fields.filter(el => el.name === name).length;
        });
        return count <= 1;
    }
  }
}
