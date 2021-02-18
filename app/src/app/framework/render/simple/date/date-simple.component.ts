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

import { Component, OnInit } from '@angular/core';
import { RenderFieldComponent } from '../../fields/components.fields';

@Component({
  selector: 'cmdb-date-simple',
  templateUrl: './date-simple.component.html',
  styleUrls: ['./date-simple.component.scss']
})
export class DateSimpleComponent extends RenderFieldComponent implements OnInit {

  constructor() {
    super();
  }

  public ngOnInit(): void {
    const dateValue = this.data ? this.data.value : this.data.value;
    if (dateValue) {
      if (dateValue.$date) {
        this.data.value = moment(new Date(dateValue.$date)).format('DD/MM/YYYY');
      } else {
        this.data.value = moment(new Date(dateValue)).format('DD/MM/YYYY');
      }
    } else {
      this.data.value = 'no date set';
    }
  }
}
