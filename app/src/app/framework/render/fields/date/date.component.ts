import { Component, OnInit } from '@angular/core';
import { RenderField } from '../components.fields';
import { formatDate } from '@angular/common';
import { NgbDateAdapter, NgbDateNativeAdapter, NgbDateStruct} from '@ng-bootstrap/ng-bootstrap';
import { NgbStringAdapter } from './NgbStringAdapter';

@Component({
  selector: 'cmdb-date',
  templateUrl: './date.component.html',
  styleUrls: ['./date.component.scss'],
  providers: [{provide: NgbDateAdapter, useClass: NgbStringAdapter}]
})
export class DateComponent extends RenderField implements  OnInit {

  public constructor() {
    super();
  }

  ngOnInit(): void {
    //format default value
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

    //format string input values to internal date model
    this.parentFormGroup.get(this.data.name).valueChanges.subscribe(value => {
      if (typeof value === 'string') {
        const pattern = RegExp('[0-9]{4}-([1-9]|0[1-9]|1[012])-([1-9]|0[1-9]|1[0-9]|2[0-9]|3[01])');
        if (pattern.test(value)) {
          const newDate = new Date(value);
          newDate.setMinutes(newDate.getMinutes() - newDate.getTimezoneOffset());
          this.parentFormGroup.get(this.data.name).setValue({$date: newDate.getTime()}, {onlySelf: true});
        } else {
          this.parentFormGroup.get(this.data.name).setErrors({'incorrect': true})
        }
      }
    });

    //trigger the conversion of string to internal date model for default value when adding new objects
    this.parentFormGroup.get(this.data.name).updateValueAndValidity({onlySelf: false,emitEvent: true });
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
