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
* along with this program. If not, see <https://www.gnu.org/licenses/>.
*/

import {
  ChangeDetectionStrategy,
  Component,
  EventEmitter, HostBinding,
  HostListener,
  Input,
  OnInit,
  Output,
  ViewEncapsulation
} from '@angular/core';
import { Column, Sort, SortDirection } from '../../table.types';

@Component({
  // tslint:disable-next-line:component-selector
  selector: 'th[table-column-head]',
  templateUrl: './table-column-head.component.html',
  styleUrls: ['./table-column-head.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush,
  encapsulation: ViewEncapsulation.Emulated
})
export class TableColumnHeadComponent implements OnInit {

  // noinspection JSMismatchedCollectionQueryUpdate
  @HostBinding('class') private cssClasses: Array<string>;
  @HostBinding('class.sortable') private sortable: boolean = false;
  @HostBinding('class.hidden') private hidden: boolean = false;

  public column: Column;

  @Input('column')
  public set Column(c: Column) {
    this.column = c;
    this.hidden = this.column.hidden;
    this.sortable = this.column.sortable || false;
    this.cssClasses = this.column.cssClasses || [];
  }

  @Input() order: SortDirection = SortDirection.NONE;

  public selected: boolean = false;

  @Input('selected')
  public set Selected(value: boolean) {
    this.onSelectedChange(value);
  }

  public onSelectedChange(value: boolean) {
    this.selected = value;
    if (!this.selected) {
      this.order = SortDirection.NONE;
    } else {
      this.order = this.reverseOrder(this.order);
    }
  }

  @Output() private sortChange: EventEmitter<Sort> = new EventEmitter<Sort>();

  @HostListener('click', ['$event'])
  public onClick(e) {
    if (this.column && this.column.sortable && this.sortable) {
      this.onSelectedChange(true);
      const sort = {
        name: this.column.data,
        order: this.order
      } as Sort;
      this.sortChange.emit(sort);
    }
  }


  public reverseOrder(direction: SortDirection): SortDirection {
    if (direction === SortDirection.DESCENDING) {
      return SortDirection.ASCENDING;
    } else {
      return SortDirection.DESCENDING;
    }
  }


  constructor() {
  }

  ngOnInit() {
  }

}
