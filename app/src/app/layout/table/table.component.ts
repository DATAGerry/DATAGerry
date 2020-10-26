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
  Component, ComponentFactoryResolver,
  ElementRef,
  EventEmitter, Injector,
  Input,
  OnDestroy,
  OnInit,
  Output,
  ViewChild,
  ViewEncapsulation
} from '@angular/core';
import { ReplaySubject } from 'rxjs';
import { Column, PageLengthEntry, Sort, TableConfig } from './models';
import { FormControl, FormGroup } from '@angular/forms';
import { debounceTime, takeUntil } from 'rxjs/operators';

export function calculateTotalPages(totalItems: number, pageLength: number): number {
  return Math.ceil(totalItems / pageLength);
}

@Component({
  selector: 'cmdb-table',
  templateUrl: './table.component.html',
  styleUrls: ['./table.component.scss'],
  encapsulation: ViewEncapsulation.None,
  changeDetection: ChangeDetectionStrategy.Default,
})
export class TableComponent<T> implements OnInit, OnDestroy {

  @Input() public tableConfig: TableConfig<T> = new TableConfig<T>();

  @Input() public columns: Array<Column> = [];
  @Input() public items: Array<T> = this.tableConfig.items;
  @Input() public totalItems: number = this.items.length;
  @Input() public pageLength: number = this.tableConfig.pageLength;
  @Input() public currentPage: number = this.tableConfig.currentPage;

  @Input() public pageLengthList: Array<PageLengthEntry> =
    [
      { label: '10', value: 10 },
      { label: '25', value: 10 },
      { label: '50', value: 10 },
      { label: '100', value: 10 },
      { label: '200', value: 10 },
      { label: '500', value: 10 },
      { label: 'All', value: 0 }
    ];
  @Input() public totalPages: number = calculateTotalPages(this.totalItems, this.pageLength);
  @Input() public maxPages: number = 5;

  @Input() public pageLengthEnabled: boolean = true;
  @Input() public searchEnabled: boolean = true;
  @Input() public paginationEnabled: boolean = true;

  @Input() public columnToggle: boolean = false;
  @Input() public searchDebounceTime: number = 500;

  @Input() public emptyItemMessage: string = 'Table list is empty!';

  @Output() public configChange: EventEmitter<void> = new EventEmitter<void>();

  @Output() public sortChange: EventEmitter<Sort> = new EventEmitter<Sort>();
  @Output() public pageLengthChange: EventEmitter<number> = new EventEmitter<number>();
  @Output() public pageChange: EventEmitter<number> = new EventEmitter<number>();
  @Output() public searchChange: EventEmitter<string> = new EventEmitter<string>();

  private subscriber: ReplaySubject<void> = new ReplaySubject<void>();

  constructor(public factory: ComponentFactoryResolver, public injector: Injector) {

  }

  public ngOnInit(): void {

  }

  public ngOnDestroy(): void {
    this.subscriber.next();
    this.subscriber.complete();
  }

  public emitPageLengthChange(value: number): void {
    this.pageLengthChange.emit(value);
  }

  public setPage(page: number): void {
    if (page < 1) {
      this.currentPage = 1;
    } else if (page > this.totalPages) {
      this.currentPage = this.totalPages;
    }
    this.emitPageChange(this.currentPage);
  }

  public emitPageChange(page: number): void {
    this.pageChange.emit(page);
  }

  public get toggleColumns(): Array<Column> {
    return this.columns.filter(c => c.fixed !== true);
  }

  /**
   * Resolve object path
   */
  public resolve(path, obj = this, separator = '.') {
    const properties = Array.isArray(path) ? path : path.split(separator);
    return properties.reduce((prev, curr) => prev && prev[curr], obj);
  }

  public get pager(): any {
    let startPage: number;
    let endPage: number;
    if (this.totalPages <= this.maxPages) {
      startPage = 1;
      endPage = this.totalPages;
    } else {
      const maxPagesBeforeCurrentPage = Math.floor(this.maxPages / 2);
      const maxPagesAfterCurrentPage = Math.ceil(this.maxPages / 2) - 1;
      if (this.currentPage <= maxPagesBeforeCurrentPage) {
        startPage = 1;
        endPage = this.maxPages;
      } else if (this.currentPage + maxPagesAfterCurrentPage >= this.totalPages) {
        startPage = this.totalPages - this.maxPages + 1;
        endPage = this.totalPages;
      } else {
        startPage = this.currentPage - maxPagesBeforeCurrentPage;
        endPage = this.currentPage + maxPagesAfterCurrentPage;
      }
    }

    const startIndex = (this.currentPage - 1) * this.pageLength;
    const endIndex = Math.min(startIndex + this.pageLength - 1, this.totalItems - 1);

    // create an array of pages to ng-repeat in the pager control
    const pages = Array.from(Array((endPage + 1) - startPage).keys()).map(i => startPage + i);
    return {
      pages
    };
  }

}
