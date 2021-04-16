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

@Component({
  template: ``
})
export class ConfigEditBaseComponent {

  public MODES = CmdbMode;
  @Input() public mode: CmdbMode = CmdbMode.Create;

  private editable: false;

  @Input() public types: Array<CmdbType> = [];

  public constructor() {
  }

  public data: any;

  @Input('data')
  public set Data(d: any) {
    this.data = d;
  }


  public sections: Array<any>;

  @Input('sections')
  public set Sections(s: Array<any>) {
    this.sections = s;
  }

  public fields: Array<any> = [];

  @Input('fields')
  public set Fields(f: Array<any>) {
    this.fields = f;
  }

  @Input('canEdit')
  public set canEdit(value: any) {
    this.editable = value;
  }

  public get canEdit(): any {
    return this.editable;
  }

  public calculateName(value) {
    if (this.canEdit) {
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
