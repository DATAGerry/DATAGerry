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

import {Component, Input, OnInit} from '@angular/core';
import { RenderField } from '../../fields/components.fields';

@Component({
  selector: 'cmdb-input-appends',
  templateUrl: './input-appends.component.html',
  styleUrls: ['./input-appends.component.scss']
})
export class InputAppendsComponent {

  public dataBind: any;
  public formGroup: any;
  public controller: any;

  @Input('data')
  public set data(value: any) {
    this.dataBind = value;
  }

  public get data(): any {
    return this.dataBind;
  }

  @Input('parentFormGroup')
  public set parentFormGroup(value: any) {
    this.formGroup = value;
  }

  public get parentFormGroup(): any {
    return this.formGroup;
  }

  @Input('controll')
  public set controll(value: any) {
    this.controller = value;
  }

  public get controll(): any {
    return this.controller;
  }

  constructor() {
  }

  public changeValueToDefault() {
    this.controller.setValue(this.data.default);
    this.controller.markAsDirty({onlySelf: true});
    this.controller.markAsTouched({onlySelf: true});
    this.parentFormGroup.markAsTouched({onlySelf: true});
    this.parentFormGroup.markAsDirty({onlySelf: true});
  }
}
