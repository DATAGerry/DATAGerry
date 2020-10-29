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

import { ChangeDetectionStrategy, Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { PageLengthEntry } from '../../components/table-page-size/table-page-size.component';
import { Column } from '../../table.types';

@Component({
  // tslint:disable-next-line:component-selector
  selector: 'table-header',
  templateUrl: './table-header.component.html',
  styleUrls: ['./table-header.component.scss'],
  changeDetection: ChangeDetectionStrategy.Default,
})
export class TableHeaderComponent implements OnInit {

  @Input() public columns: Array<Column>;
  @Input() public toggleable: boolean = false;

  @Input() public pageSizeEnabled: boolean = true;
  @Input() public searchEnabled: boolean = true;

  @Input() public debounceTime: number;

  @Input() public pageSize: number;
  @Input() public pageSizeList: Array<PageLengthEntry>;

  @Output() public searchChange: EventEmitter<string> = new EventEmitter<string>();
  @Output() public pageSizeChange: EventEmitter<number> = new EventEmitter<number>();

  constructor() { }

  ngOnInit() {
  }

}
