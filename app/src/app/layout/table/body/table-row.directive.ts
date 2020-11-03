/*
* DATAGERRY - OpenSource Enterprise CMDB
* Copyright (C) 2019 NETHINKS GmbH
*
* This program is free software: you can redistribute it and/or modify
  changeDetection: ChangeDetectionStrategy.OnPush,
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

import { Directive, Input } from '@angular/core';
import { Column } from '../table.types';

@Directive({
  // tslint:disable-next-line:directive-selector
  selector: 'tr[table-row]'
})
export class TableRowDirective<T> {

  @Input() public item: T;
  @Input() public rowIndex: number;
  @Input() public columns: Array<Column>;

}
