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

import {NgbDateAdapter, NgbDateParserFormatter, NgbDateStruct} from '@ng-bootstrap/ng-bootstrap';
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
        day: date.getDate(),
        month: date.getMonth() + 1,
        year: date.getFullYear()
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


/**
 * This Service handles how the date is rendered and parsed from keyboard i.e. in the bound input field.
 */
@Injectable()
export class CustomDateParserFormatter extends NgbDateParserFormatter {

  readonly DELIMITER = '/';

  parse(value: string): NgbDateStruct | null {
    if (value) {
      const date = value.split(this.DELIMITER);
      return {
        day : parseInt(date[0], 10),
        month : parseInt(date[1], 10),
        year : parseInt(date[2], 10)
      };
    }
    return null;
  }

  padNumber(value: number) {
    if (this.isNumber(value)) {
      return `0${value}`.slice(-2);
    } else {
      return value;
    }
  }

  isNumber(value: any): boolean {
    return !isNaN(this.toInteger(value));
  }

  toInteger(value: any): number {
    return parseInt(`${value}`, 10);
  }

  format(date: NgbDateStruct | null): string {
    return date ? date.day + this.DELIMITER + this.padNumber(date.month) + this.DELIMITER + date.year : null;
  }
}
