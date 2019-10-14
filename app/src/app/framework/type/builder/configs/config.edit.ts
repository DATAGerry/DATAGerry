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
import {Input} from '@angular/core';
import {CmdbMode} from '../../../modes.enum';

export class ConfigEdit {
  private innerData: any;
  private editActive: false;

  public constructor() {
  }

  @Input('data')
  public set data(value: any) {
    this.innerData = value;
  }

  public get data(): any {
    return this.innerData;
  }

  @Input('activeEdit')
  public set activeEdit(value: any) {
    this.editActive = value;
  }

  public get activeEdit(): any {
    return this.editActive;
  }

  public calculateName(value) {
    if (this.activeEdit) {
      this.data.name = value.replace(/ /g, '-').toLowerCase();
    }
  }
}
