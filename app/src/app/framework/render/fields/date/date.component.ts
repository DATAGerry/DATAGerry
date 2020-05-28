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
    if (this.data.default !== undefined) {
      const temp = this.data.default;
      this.data.default = temp.year + '-' + temp.month + '-' + temp.day;
      if (typeof temp === 'string') {
        const newDate = new Date(temp);
        this.parentFormGroup.get(this.data.name).setValue({$date: newDate.getTime()}, {onlySelf: true});
      }
    }
    if (this.parentFormGroup.get(this.data.name).value === '') {
      this.parentFormGroup.get(this.data.name).setValue(null, {onlySelf: true});
    }
    this.parentFormGroup.get(this.data.name).valueChanges.subscribe(value => {
      if (typeof value === 'string') {
        const newDate = new Date(value);
        this.data.value = {$date: newDate.getTime()};
        this.parentFormGroup.get(this.data.name).setValue({$date: newDate.getTime()}, {onlySelf: true});
      }
    });
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
