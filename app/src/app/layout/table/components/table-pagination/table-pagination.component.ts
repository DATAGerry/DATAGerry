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

export interface Pager {
  totalItems: number;
  currentPage: number;
  pageSize: number;
  totalPages: number;
  startPage: number;
  endPage: number;
  startIndex: number;
  endIndex: number;
  pages: Array<number>;
}

@Component({
  // tslint:disable-next-line:component-selector
  selector: 'table-pagination',
  templateUrl: './table-pagination.component.html',
  styleUrls: ['./table-pagination.component.scss']
})
export class TablePaginationComponent implements OnInit, OnChanges {

  private readonly initPage: number = 1;
  public currentPage: number = this.initPage;

  @Input('currentPage')
  public set CurrentPage(page: number) {
    this.currentPage = page || this.initPage;
  }

  public totalItems: number = 0;

  @Input('totalItems')
  public set TotalItems(total: number) {
    this.totalItems = total || 0;
  }

  public pageSize: number = 10;

  @Input('pageSize')
  public set PageSize(size: number) {
    this.pageSize = size || 10;
  }

  public maxPages: number = 5;

  @Input('maxPages')
  public set MaxPages(max: number) {
    this.maxPages = max || 5;
  }

  public pager: Pager;

  @Output() public pageChange: EventEmitter<number> = new EventEmitter<number>();

  public ngOnInit(): void {
    this.pager = this.paginate(this.currentPage);
  }

  public ngOnChanges(changes: SimpleChanges): void {
    this.pager = this.paginate(this.currentPage);
  }

  public setPage(page: number): void {
    if (page < 1) {
      this.currentPage = 1;
    } else if (page > this.pager.totalPages) {
      this.currentPage = this.pager.totalPages;
    } else{
      this.currentPage = page;
    }
    this.pager = this.paginate(this.currentPage);
    this.pageChange.emit(this.currentPage);
  }

  public paginate(currentPage: number = 1): Pager {

    const pageSize = this.pageSize;
    const maxPages = this.maxPages;
    const totalItems = this.totalItems;
    const totalPages = Math.ceil(this.totalItems / pageSize);

    if (currentPage < 1) {
      currentPage = 1;
    } else if (currentPage > totalPages) {
      currentPage = totalPages;
    }

    let startPage: number;
    let endPage: number;
    if (totalPages <= maxPages) {
      startPage = 1;
      endPage = totalPages;
    } else {
      const maxPagesBeforeCurrentPage = Math.floor(maxPages / 2);
      const maxPagesAfterCurrentPage = Math.ceil(maxPages / 2) - 1;
      if (currentPage <= maxPagesBeforeCurrentPage) {
        startPage = 1;
        endPage = maxPages;
      } else if (currentPage + maxPagesAfterCurrentPage >= totalPages) {
        startPage = totalPages - maxPages + 1;
        endPage = totalPages;
      } else {
        startPage = currentPage - maxPagesBeforeCurrentPage;
        endPage = currentPage + maxPagesAfterCurrentPage;
      }
    }

    const startIndex = (currentPage - 1) * pageSize;
    const endIndex = Math.min(startIndex + pageSize - 1, totalItems - 1);
    const pages = Array.from(Array((endPage + 1) - startPage).keys()).map(i => startPage + i);

    return {
      totalItems,
      currentPage,
      pageSize,
      totalPages,
      startPage,
      endPage,
      startIndex,
      endIndex,
      pages
    } as Pager;
  }

}
