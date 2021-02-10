import { NgbDateAdapter, NgbDateStruct } from '@ng-bootstrap/ng-bootstrap';
import { Injectable } from '@angular/core';

@Injectable()
export class NgbStringAdapter extends NgbDateAdapter<Date> {

  parse(value: string): NgbDateStruct {
    return null;
  }

  fromModel(date: any): NgbDateStruct {
    if (typeof date === 'string') {
      const newDate =  new Date(date);
      return newDate ? {
        year: newDate.getFullYear(),
        month: newDate.getMonth() + 1,
        day: newDate.getDate()
      } : null;
    } else if (date != null) {
      date = new Date(date.$date);
      return date ? {
        year: date.getFullYear(),
        month: date.getMonth() + 1,
        day: date.getDate()
      } : null;
    }
    return null;
  }

  toModel(date: NgbDateStruct): any {
    if (date != null) {
      const d = new Date(date.year, date.month - 1, date.day);
      d.setMinutes(d.getMinutes() - d.getTimezoneOffset());
      return {$date: d.getTime()};
    }
    return null;
  }
}
