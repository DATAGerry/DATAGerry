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

@Component({
  selector: 'cmdb-object-bulk-input-appends',
  templateUrl: './object-bulk-input-appends.component.html',
  styleUrls: ['./object-bulk-input-appends.component.scss']
})
export class ObjectBulkInputAppendsComponent implements OnInit {

  public dataBind: any;
  public formGroup: any;
  public controller: any;
  public bulkControlName: string;

  @Input('data')
  public set data(value: any) {
    this.dataBind = value;
    this.bulkControlName = value.name + '-isChanged';
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

  ngOnInit() {
    this.controller.valueChanges.subscribe(value => {
      this.parentFormGroup.get(this.bulkControlName).setValue(true);
      this.parentFormGroup.get('changedFields').value.set(this.data.name, this.data);
    });
  }

  public changeCheckBox(value: any) {
    if (value.checked) {
      this.parentFormGroup.get('changedFields').value.set(this.data.name, this.data);
    } else {
      this.parentFormGroup.get('changedFields').value.delete(this.data.name);
      this.parentFormGroup.get(this.data.name).markAsUntouched({onlySelf: true});
      this.parentFormGroup.get(this.data.name).setErrors(null);
    }
  }
}
