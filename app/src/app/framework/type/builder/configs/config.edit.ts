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
* along with this program.  If not, see <https://www.gnu.org/licenses/>.
*/

import {Component, Input} from '@angular/core';

@Component({
  template: ''
})
export class ConfigEditBaseComponent {
  private innerData: any;
  private innerSections: any[];
  private editable: false;

  public constructor() {
  }

  @Input('data')
  public set data(value: any) {
    this.innerData = value;
  }

  public get data(): any {
    return this.innerData;
  }

  @Input('sections')
  public set sections(value: any) {
    this.innerSections = value;
  }

  public get sections(): any {
    return this.innerSections;
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
    const {type, name} = this.data;
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
