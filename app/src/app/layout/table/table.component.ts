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
  Component, ElementRef,
  EventEmitter,
  Input, isDevMode,
  OnDestroy,
  OnInit,
  Output, ViewChild,
  ViewEncapsulation
} from '@angular/core';
import { ReplaySubject } from 'rxjs';
import { Column, Sort, SortDirection } from './table.types';
import { takeUntil } from 'rxjs/operators';
import { PageLengthEntry } from './components/table-page-size/table-page-size.component';

@Component({
  selector: 'cmdb-table',
  templateUrl: './table.component.html',
  styleUrls: ['./table.component.scss'],
  encapsulation: ViewEncapsulation.None,
  changeDetection: ChangeDetectionStrategy.Default,
})
export class TableComponent<T> implements OnInit, OnDestroy {

  /**
   * `ViewChild` for accessing the complete table container.
   */
  @ViewChild('container', { static: true }) public containerRef: ElementRef;

  /**
   * `ViewChild` for accessing the table html element.
   */
  @ViewChild('table', { static: true }) public tableRef: ElementRef;

  /**
   * Component un subscriber.
   * @private
   */
  private subscriber: ReplaySubject<void> = new ReplaySubject<void>();

  /**
   * Message which will be shown if no data are in the table.
   */
  @Input() public emptyMessage: string = 'No data to display!';

  /**
   * Component wide debounce time.
   */
  @Input() public debounceTime: number = 500;

  /**
   * Is the table data currently in loading.
   */
  @Input() public loading: boolean = false;

  /**
   * Should the loading spinner be loaded.
   */
  @Input() public loadingEnabled: boolean = true;

  /**
   * Columns
   */
  public columns: Array<Column> = [];

  /**
   * Column holder for reset.
   * @private
   */
  private initialColumns: Array<Column> = [];

  /**
   * Column setter.
   *
   * @param columns
   */
  @Input('columns')
  public set Columns(columns: Array<Column>) {
    this.columns = columns;
    this.initialColumns = this.columns;
  }

  /**
   * Items or data which will be inserted into the tbody.
   */
  @Input() public items: Array<T> = [];

  /**
   * Total number of items which exists for this table.
   */
  @Input() public totalItems: number = 0;

  /**
   * Is row selected enabled.
   */
  @Input() public selectEnabled: boolean = false;

  /**
   * Selected items.
   */
  @Input() public selectedItems: Array<T> = [];

  /**
   * Event emitter when selected items changed.
   */
  @Output() public selectedChange: EventEmitter<Array<T>> = new EventEmitter<Array<T>>();

  /**
   * Current displayed page number.
   */
  @Input() public currentPage: number = 1;

  /**
   * Pagination enabled.
   */
  @Input() public paginationEnabled: boolean = true;

  /**
   * Event Emitter when the current page was changed.
   */
  @Output() public pageChange: EventEmitter<number> = new EventEmitter<number>();

  /**
   * Is a switching of the page size possible.
   */
  @Input() public pageSizeEnabled: boolean = true;

  /**
   * Current page size.
   */
  @Input() public pageSize: number = 10;

  /**
   * Possible page size list.
   */
  @Input() public pageSizeList: Array<PageLengthEntry>;

  /**
   * Event Emitter when the page size changed.
   */
  @Output() public pageSizeChange: EventEmitter<number> = new EventEmitter<number>();

  /**
   * Search input enabled.
   */
  @Input() public searchEnabled: boolean = true;

  /**
   * Event Emitter for search input change.
   */
  @Output() public searchChange: EventEmitter<string> = new EventEmitter<string>();

  /**
   * Info display enabled.
   */
  @Input() public infoEnabled: boolean = true;

  /**
   * Are columns toggleable.
   */
  @Input() public toggleable: boolean = false;

  /**
   * Dynamic list of css classes for the table body.
   */
  @Input() public bodyClasses: Array<string> = [];

  /**
   * Dynamic list of css classes for column heads.
   */
  @Input() public columnClasses: Array<string> = [];

  /**
   * Dynamic list of css classes for rows.
   */
  @Input() public rowClasses: Array<string> = [];

  /**
   * Sorting enabled.
   */
  @Input() public sortable: boolean = true;

  /**
   * Sort change emitter.
   */
  @Output() public sortChange: EventEmitter<Sort> = new EventEmitter<Sort>();

  /**
   * Table sort value.
   */
  public sort: Sort = { name: null, order: SortDirection.NONE };

  /**
   * Sort input setter.
   * @param value
   */
  @Input('sort')
  public set Sort(value: Sort) {
    this.sort = value;
  }

  /**
   * Function when on sort changed emitter.
   * @param sort
   */
  public onSortChange(sort: Sort): void {
    this.sort = sort;
    this.sortChange.emit(sort);
  }

  public ngOnInit(): void {
    if (isDevMode()) {
      this.pageSizeChange.asObservable().pipe(takeUntil(this.subscriber)).subscribe((size: number) => {
        console.log(`[TableEvent] Page size changed to: ${ size }`);
      });
      this.pageChange.asObservable().pipe(takeUntil(this.subscriber)).subscribe((page: number) => {
        console.log(`[TableEvent] Page changed to: ${ page }`);
      });
      this.searchChange.asObservable().pipe(takeUntil(this.subscriber)).subscribe((search: string) => {
        console.log(`[TableEvent] Search input changed to: ${ search }`);
      });
      this.selectedChange.asObservable().pipe(takeUntil(this.subscriber)).subscribe((selected: Array<T>) => {
        console.log(`[TableEvent] Selected rows changed to`);
        console.log(selected);
      });
      this.sortChange.asObservable().pipe(takeUntil(this.subscriber)).subscribe((sort: Sort) => {
        console.log(`[TableEvent] Sort changed to:`);
        console.log(sort);
      });
    }

  }

  public toggleRowSelection(item: T, event: any): void {
    const checked = event.currentTarget.checked;
    if (checked) {
      this.selectedItems.push(item);
    } else {
      const idx = this.selectedItems.indexOf(item);
      if (idx !== -1) {
        this.selectedItems.splice(idx, 1);
      }
    }
    this.selectedChange.emit(this.selectedItems);
  }

  public toggleAllRowSelections(event: any): void {
    const checked = event.currentTarget.checked;
    if (checked) {
      this.selectedItems = [...this.items];
    } else {
      this.selectedItems = [];
    }
    this.selectedChange.emit(this.selectedItems);
  }

  public onColumnVisibilityChange(column: Column) {
    const col = this.columns.find(c => c.name === column.name);
    const colIndex = this.columns.indexOf(col);
    this.columns[colIndex].hidden = column.hidden;
  }


  /**
   * Reset the columns to the initial set.
   */
  public onColumnsReset(): void {
    this.columns = this.initialColumns;
  }

  public onPageChange(page: number) {
    this.selectedItems = [];
    this.pageChange.emit(page);
  }

  public ngOnDestroy(): void {
    this.subscriber.next();
    this.subscriber.complete();
  }


}
