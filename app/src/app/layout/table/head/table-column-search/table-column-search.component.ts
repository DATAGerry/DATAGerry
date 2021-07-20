/*
* DATAGERRY - OpenSource Enterprise CMDB
* Copyright (C) 2021 NETHINKS GmbH
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

import {
  ChangeDetectionStrategy,
  Component,
  EventEmitter,
  Input,
  Output, ViewEncapsulation
} from '@angular/core';
import { Column } from '../../table.types';
import { FormGroup } from '@angular/forms';
import { ReplaySubject } from 'rxjs';

@Component({
  // tslint:disable-next-line:component-selector
  selector: 'th[table-column-search]',
  templateUrl: './table-column-search.component.html',
  styleUrls: ['./table-column-search.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush,
  encapsulation: ViewEncapsulation.Emulated
})
export class TableColumnSearchComponent<T> {

  /**
   * Column search form group.
   */
  @Input() form: FormGroup;

  /**
   * Column of this head element.
   */
  public column: Column;

  /**
   * Column setter. Also sets the `hidden`, `sortable` and `cssClasses`
   * property from the Column element.
   * @param c Column
   */
  @Input('column')
  public set Column(c: Column) {
    this.column = c;
  }
}
