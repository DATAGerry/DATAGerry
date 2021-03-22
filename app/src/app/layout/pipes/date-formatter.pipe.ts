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
* along with this program. If not, see <https://www.gnu.org/licenses/>.
*/

import * as moment from 'moment';
import { Pipe, PipeTransform } from '@angular/core';
import { DateSettingsService} from '../../settings/services/date-settings.service';

@Pipe({
  name: 'dateFormatter'
})
export class DateFormatterPipe implements PipeTransform {

  constructor(private dateSettingsService: DateSettingsService) {
  }

  /**
   * Converts input date string representation of the date according to the selected pattern
   */
  transform(data: any): any {
    const { timezone, date_format } = this.dateSettingsService.currentDateSettings;
    const date = moment.utc(data);
    return date.isValid() ? moment.tz(date, timezone).format(date_format) : data;
  }

}
