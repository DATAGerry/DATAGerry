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
import { zip, Observable, ReplaySubject, merge } from 'rxjs';
import { Column, Sort, SortDirection, TableConfig, TableConfigUserSetting } from './table.types';
import { PageLengthEntry } from './components/table-page-size/table-page-size.component';
import { takeUntil } from 'rxjs/operators';

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
   * html table id
   */
  @Input() public id: string = `table-${ Math.random().toString(36).substring(10) }`;

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
    this.initialColumns = Object.assign([], []);
    this.items = [];
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
   * Initial page site
   */
  public initPage: number = 1;

  @Input('initPage')
  public set Page(page: number) {
    this.initPage = page;
    this.page = page;
  }

  /**
   * Current displayed page number.
   */
  public page: number = 1;

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
   * Event emitter when any config was changed.
   */
  @Input() public configEnabled: boolean = true;

  /**
   * List of possible table configs.
   */
  @Input() public tableConfigs: Array<TableConfigUserSetting> = [];

  /**
   * Event emitter when any config was changed.
   */
  @Output() public configChange: EventEmitter<TableConfigUserSetting> = new EventEmitter<TableConfigUserSetting>();

  /**
   * Current user table config.
   */
  @Input() public userTableConfig: TableConfigUserSetting;

  /**
   * Visibility change emitter.
   */
  @Output() public columnVisibilityChange: EventEmitter<Column> = new EventEmitter<Column>();

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
    this.configChangeObservable.pipe(takeUntil(this.subscriber)).subscribe(() => {
      const tableConfig: TableConfig = {
        columns: this.columns,
        page: this.page,
        pageSize: this.pageSize,
        sort: this.sort
      } as TableConfig;
      this.userTableConfig = {
        label: '',
        data: tableConfig,
        active: true
      } as TableConfigUserSetting;
      this.configChange.emit(this.userTableConfig);
    });
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

  /**
   * Get any kind of table config change as observable.
   * @private
   */
  private get configChangeObservable(): Observable<any> {
    return merge(
      this.pageChange.asObservable(),
      this.columnVisibilityChange.asObservable(),
      this.sortChange.asObservable(),
      this.pageSizeChange.asObservable()
    );
  }

  /**
   * Toggle the selection of a single row.
   * @param item presented item in this row
   * @param event checkbox change event
   */
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

  /**
   * Toggle the selection of all displayed elements.
   * @param event global checkbox change event
   */
  public toggleAllRowSelections(event: any): void {
    const checked = event.currentTarget.checked;
    if (checked) {
      this.selectedItems = [...this.items];
    } else {
      this.selectedItems = [];
    }
    this.selectedChange.emit(this.selectedItems);
  }

  /**
   * On hidden status change of a column.
   * @param column with changed hidden status.
   */
  public onColumnVisibilityChange(column: Column) {
    const col = this.columns.find(c => c.name === column.name);
    const colIndex = this.columns.indexOf(col);
    this.columns[colIndex].hidden = column.hidden;
    this.columnVisibilityChange.emit(column);
  }


  /**
   * Reset the columns to the initial set.
   */
  public onColumnsReset(): void {
    this.columns = Object.assign([], this.initialColumns);
  }

  /**
   * Page change.
   * @param page new page number
   */
  public onPageChange(page: number) {
    this.selectedItems = [];
    this.page = page;
    this.pageChange.emit(page);
  }

  public onConfigSave(config: TableConfigUserSetting) {
    console.log(config);
  }

  public ngOnDestroy(): void {
    this.subscriber.next();
    this.subscriber.complete();
  }


}
