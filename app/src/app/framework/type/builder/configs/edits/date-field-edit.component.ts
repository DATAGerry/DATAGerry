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

import { Component, Input } from '@angular/core';
import { ConfigEditBaseComponent } from '../config.edit';
import { NgbDateAdapter, NgbDateParserFormatter } from '@ng-bootstrap/ng-bootstrap';
import { CustomDateParserFormatter, NgbStringAdapter } from '../../../../render/fields/date/date-formatter-adapter';

@Component({
  selector: 'cmdb-date-field-edit',
  templateUrl: './date-field-edit.component.html',
  styleUrls: ['./date-field-edit.component.scss'],
  providers: [
    {provide: NgbDateAdapter, useClass: NgbStringAdapter},
    {provide: NgbDateParserFormatter, useClass: CustomDateParserFormatter}
  ]
})
export class DateFieldEditComponent extends ConfigEditBaseComponent {

  @Input() groupList: any;
  @Input() userList: any;

  constructor() {
    super();
  }

  public resetDate() {
    this.data.value = null;
  }

}
