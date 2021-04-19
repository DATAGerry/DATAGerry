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

import { Component, Input, OnInit } from '@angular/core';
import { ConfigEditBaseComponent } from '../config.edit';

@Component({
  selector: 'cmdb-text-field-edit',
  templateUrl: './text-field-edit.component.html',
  styleUrls: ['./text-field-edit.component.scss']
})
export class TextFieldEditComponent extends ConfigEditBaseComponent implements OnInit {

  public regexValid: boolean;

  constructor() {
    super();
  }

  public ngOnInit(): void {
    this.regexValid = true;
  }

  public validateRegex(regex: string) {
    try {
      // tslint:disable-next-line:no-unused-expression
      new RegExp(regex);
      this.regexValid = true;
    } catch (e) {
      this.regexValid = false;
    }
  }

}
