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

import { ChangeDetectionStrategy, Component, HostListener, Input, OnInit, ViewEncapsulation } from '@angular/core';
import { Column } from '../../models';

@Component({
  // tslint:disable-next-line:component-selector
  selector: 'th[table-column-head]',
  templateUrl: './table-column-head.component.html',
  styleUrls: ['./table-column-head.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush,
  encapsulation: ViewEncapsulation.Emulated
})
export class TableColumnHeadComponent implements OnInit {

  @Input() public column: Column;
  @Input() sortSelected: boolean = false;
  @Input() sortDirection: number = 1;

  @HostListener('click', ['$event'])
  public onClick(e) {
    if (this.column && this.column.sortable) {
      this.sortSelected = true;
    }
  }


  constructor() {
  }

  ngOnInit() {
  }

}
