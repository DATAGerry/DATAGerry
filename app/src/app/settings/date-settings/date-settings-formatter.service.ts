/*
* DATAGERRY - OpenSource Enterprise CMDB
* Copyright (C) 2019 - 2021 NETHINKS GmbH
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

import * as moment from 'moment';
import 'moment-timezone';
import { NgbDateAdapter, NgbDateParserFormatter, NgbDateStruct } from '@ng-bootstrap/ng-bootstrap';
import { Injectable } from '@angular/core';

/**
 * This Service handles how the date is represented in scripts i.e. ngModel.
 */
@Injectable()
export class NgbStringAdapter extends NgbDateAdapter<Date> {

  fromModel(date: any): NgbDateStruct {
    if (typeof date === 'string') {
      const newDate =  new Date(date);
      return newDate ? {
        day: newDate.getDate(),
        month: newDate.getMonth() + 1,
        year: newDate.getFullYear(),
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

  /**
   * Convert the transferred date to timestamp for Database
   * @param date
   */
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

  parse(value: string): NgbDateStruct | null {
    return null;
  }

  /**
   * String representation of the date according to the selected pattern
   * When creating a moment from a string, we first check if the string matches known ISO 8601 formats,
   * we then check if the string matches the RFC 2822 Date time format before dropping to the fall back
   * of new Date(string) if a known format is not found.
   * @param date
   */
  format(date: NgbDateStruct | null): string {
    return date ? moment.tz(moment(new Date(Date.UTC(date.year, date.month - 1, date.day))), 'Europe/Berlin')
      .format('YYYY-MM-DDThh:mm:ss' + '( UTC Z )') : null;
  }
}
