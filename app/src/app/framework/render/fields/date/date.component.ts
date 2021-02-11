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


import { Component, OnInit } from '@angular/core';
import { RenderFieldComponent } from '../components.fields';
import { formatDate } from '@angular/common';
import { NgbDateAdapter, NgbDateParserFormatter } from '@ng-bootstrap/ng-bootstrap';
import { CustomDateParserFormatter, NgbStringAdapter } from './NgbStringAdapter';

@Component({
  selector: 'cmdb-date',
  templateUrl: './date.component.html',
  styleUrls: ['./date.component.scss'],
  providers: [
    {provide: NgbDateAdapter, useClass: NgbStringAdapter},
    {provide: NgbDateParserFormatter, useClass: CustomDateParserFormatter}
    ]
})
export class DateComponent extends RenderFieldComponent implements  OnInit {

  public constructor() {
    super();
  }

  ngOnInit(): void {
    // format default value
    if (this.data.default !== undefined  && this.data.default.year && this.data.default.month && this.data.default.day) {
      const temp = this.data.default;
      this.data.default = temp.year + '-' + temp.month + '-' + temp.day;
      if (typeof temp === 'string') {
        const newDate = new Date(temp);
        newDate.setMinutes(newDate.getMinutes() - newDate.getTimezoneOffset());
        this.parentFormGroup.get(this.data.name).setValue({$date: newDate.getTime()}, {onlySelf: true});
      }
    }
    if (this.parentFormGroup.get(this.data.name).value === '') {
      this.parentFormGroup.get(this.data.name).setValue(null, {onlySelf: true});
    }

    // format string input values to internal date model
    this.parentFormGroup.get(this.data.name).valueChanges.subscribe(value => {
      if (typeof value === 'string') {
        const pattern = RegExp('[0-9]{4}-([1-9]|0[1-9]|1[012])-([1-9]|0[1-9]|1[0-9]|2[0-9]|3[01])');
        if (pattern.test(value)) {
          const newDate = new Date(value);
          newDate.setMinutes(newDate.getMinutes() - newDate.getTimezoneOffset());
          this.parentFormGroup.get(this.data.name).setValue({$date: newDate.getTime()}, {onlySelf: true});
        } else {
          this.parentFormGroup.get(this.data.name).setErrors({incorrect: true});
        }
      }
    });

    // trigger the conversion of string to internal date model for default value when adding new objects
    this.parentFormGroup.get(this.data.name).updateValueAndValidity({onlySelf: false, emitEvent: true });
  }

  public get currentDate() {
    const currentDate = this.parentFormGroup.get(this.data.name).value;
    if (currentDate && currentDate.$date) {
      return new Date(currentDate.$date);
    }
    return currentDate;
  }

  public copyToClipboard() {
    const selBox = document.createElement('textarea');
    selBox.value = formatDate(this.currentDate, 'dd/MM/yyyy', 'en-US');
    this.generateDataForClipboard(selBox);
  }
}
