/*
* dataGerry - OpenSource Enterprise CMDB
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

import { Component, Input, OnInit } from '@angular/core';

@Component({
  selector: 'cmdb-choice-field-edit',
  templateUrl: './choice-field-edit.component.html',
  styleUrls: ['./choice-field-edit.component.scss']
})
export class ChoiceFieldEditComponent implements OnInit {

  @Input() groupList: any;
  @Input() userList: any;
  @Input() data: any;
  public options = [];

  constructor() {
    this.options.push({
      name: 'option-1',
      label: 'Option 1'
    });
  }

  public ngOnInit(): void {
    this.data.options = this.options;
  }

  public addOption() {
    this.options.push({
      name: `option-${(this.options.length + 1)}`,
      label: `Option ${(this.options.length + 1)}`
    });
  }

}
