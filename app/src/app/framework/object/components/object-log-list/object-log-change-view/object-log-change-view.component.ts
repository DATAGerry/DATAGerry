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

import { Component, Input } from '@angular/core';
import { LogMode } from '../../../../modes.enum';

@Component({
  selector: 'cmdb-object-log-change-view',
  templateUrl: './object-log-change-view.component.html',
  styleUrls: ['./object-log-change-view.component.scss']
})
export class ObjectLogChangeViewComponent {

  public modes = LogMode;
  @Input() action: LogMode;
  @Input() changes: any[];


}
