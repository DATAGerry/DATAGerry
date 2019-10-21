import { Component, OnInit } from '@angular/core';
import { RenderField } from '../components.fields';
import { formatDate } from '@angular/common';

@Component({
  selector: 'cmdb-date',
  templateUrl: './date.component.html',
  styleUrls: ['./date.component.scss']
})
export class DateComponent extends RenderField implements  OnInit{
  public dateValue: any = '';

  public constructor() {
    super();
  }

  ngOnInit(): void {
  }

  public getDateValue(obj) {
    // ToDo: Recognize format by language
    if ( obj.day === undefined) {
      return 'TT.MM.JJJJ';
    }
    const format = 'dd/MM/yyyy';
    const myDate = obj.year + '-' + obj.month + '-' + obj.day;
    const locale = 'en-US';
    const formattedDate = formatDate(myDate, format, locale);
    return formattedDate;
  }
}
