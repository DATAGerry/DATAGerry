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

import { Component, EventEmitter, Input, OnChanges, OnInit, Output, SimpleChanges } from '@angular/core';

@Component({
  // tslint:disable-next-line:component-selector
  selector: 'table-footer',
  templateUrl: './table-footer.component.html',
  styleUrls: ['./table-footer.component.scss']
})
export class TableFooterComponent implements OnInit, OnChanges {

  @Input() public items: Array<any> = [];
  @Input() public paginationEnabled: boolean = true;
  @Input() public infoEnabled: boolean = true;

  @Input() public selectEnabled: boolean = false;
  @Input() public selected: number = 0;

  @Input() public currentPage: number;
  @Input() public totalItems: number;
  @Input() public pageSize: number;
  @Input() public maxPages: number;

  public show: number = 0;

  @Output() public pageChange: EventEmitter<number> = new EventEmitter<number>();

  public ngOnInit(): void {
    this.show = this.items.length;
  }

  public ngOnChanges(changes: SimpleChanges): void {
    if (changes.items && changes.items.currentValue !== changes.items.previousValue) {
      this.show = this.items.length;
    }
  }

}
