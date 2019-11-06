import {NgbDateAdapter, NgbDateStruct} from '@ng-bootstrap/ng-bootstrap';

export class NgbStringAdapter extends NgbDateAdapter<Date> {

  parse(value: string): NgbDateStruct {
    return null;
  }

  fromModel(date: any): NgbDateStruct {
    if (date && date.item) {
      const newDate =  new Date(date.item);
      return newDate ? {
        year: newDate.getFullYear(),
        month: newDate.getMonth() + 1,
        day: newDate.getDate()
      } : null;
    }

    if (typeof date === 'string') {
      const newDate =  new Date(date);
      return newDate ? {
        year: newDate.getFullYear(),
        month: newDate.getMonth() + 1,
        day: newDate.getDate()
      } : null;
    }

    if (date instanceof Date) {
      return date ? {
        year: date.getFullYear(),
        month: date.getMonth() + 1,
        day: date.getDate()
      } : null;
    }

    return null;
  }

  toModel(date: NgbDateStruct): Date {
    return date ? new Date(Date.UTC(date.year, date.month - 1, date.day, 0, 0, 0)) : null;

  }
}
