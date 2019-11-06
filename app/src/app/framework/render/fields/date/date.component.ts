import { Component, OnInit } from '@angular/core';
import { RenderField } from '../components.fields';
import { formatDate } from '@angular/common';
import {NgbDateAdapter, NgbDateNativeAdapter, NgbDateStruct} from '@ng-bootstrap/ng-bootstrap';

@Component({
  selector: 'cmdb-date',
  templateUrl: './date.component.html',
  styleUrls: ['./date.component.scss'],
  providers: [{provide: NgbDateAdapter, useClass: NgbDateNativeAdapter}]
})
export class DateComponent extends RenderField implements  OnInit {

  public constructor() {
    super();
  }

  get today() {
    return new Date();
  }


  public onDateSelect(value: any, item: any) {
    console.log(this.parentFormGroup.get(item).value);
  }

  ngOnInit(): void {
  }

}
