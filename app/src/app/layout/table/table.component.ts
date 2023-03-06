/*
* DATAGERRY - OpenSource Enterprise CMDB
* Copyright (C) 2023 becon GmbH
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
  Output, TemplateRef, ViewChild,
  ViewEncapsulation
} from '@angular/core';
import { Observable, ReplaySubject, merge } from 'rxjs';
import { Column, GroupRowsBy, Sort, SortDirection, TableState } from './table.types';
import { PageLengthEntry } from './components/table-page-size/table-page-size.component';
import { takeUntil } from 'rxjs/operators';
import { TableService } from './table.service';
import { Router } from '@angular/router';
import { FormGroup } from '@angular/forms';

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
   * Array of possible custom buttons displayed in header.
   */
  @Input() public customButtons: Array<TemplateRef<any>>;

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
   */
  @Input() public initialVisibleColumns: Array<string> = [];

  /**
   * Column setter.
   *
   * @param columns
   */
  @Input('columns')
  public set Columns(columns: Array<Column>) {
    this.columns = columns;
    this.items = [];
  }

  /**
   * Column search form group.
   */
  public columnSearchForm: FormGroup;

  /**
   * Column search columnSearchForm group.
   */
  public columnSearchIconHidden: boolean = false;

  /**
   * Column search input enabled.
   */
  @Input() public columnSearchEnabled: boolean = false;

  /**
   * Event Emitter for column search input change.
   */
  @Output() public columnSearchChange: EventEmitter<any[]> = new EventEmitter<any[]>();

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
  public set InitPage(page: number) {
    this.initPage = page;
    this.page = page;
  }

  /**
   * Current displayed page number.
   */
  public page: number = this.initPage;

  @Input('page')
  public set Page(page: number) {
    this.page = page;
  }

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
   * Row group parameter.
   */
  @Input() public groupRowsBy: GroupRowsBy;

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
   * Event emitter when any config was changed.
   */
  @Input() public stateEnabled: boolean = false;

  /**
   * List of possible table configs.
   */
  @Input() public tableStates: Array<TableState> = [];

  /**
   * Current user table config.
   */
  @Input() public tableState: TableState;

  /**
   * Event emitter when any config was changed.
   */
  @Output() public stateChange: EventEmitter<TableState> = new EventEmitter<TableState>();

  /**
   * Config save emit.
   */
  @Output() public stateSelect: EventEmitter<TableState> = new EventEmitter<TableState>();
  @Output() public stateSave: EventEmitter<TableState> = new EventEmitter<TableState>();
  @Output() public stateUpdate: EventEmitter<TableState> = new EventEmitter<TableState>();
  @Output() public stateDelete: EventEmitter<TableState> = new EventEmitter<TableState>();
  @Output() public stateReset: EventEmitter<void> = new EventEmitter<void>();

  public constructor(private tableService: TableService, private router: Router) {
  }

  public ngOnInit(): void {
    this.configChangeObservable.pipe(takeUntil(this.subscriber)).subscribe(() => {
      this.tableState = {
        name,
        page: this.page,
        pageSize: this.pageSize,
        sort: this.sort,
        visibleColumns: this.columns.filter(c => !c.hidden).map(c => c.name)
      } as TableState;
      if (this.stateEnabled) {
        this.tableService.setCurrentTableState(this.router.url, this.id, this.tableState);
        this.stateChange.emit(this.tableState);
      }
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
    for (const col of this.columns) {
      col.hidden = !this.initialVisibleColumns.includes(col.name);
    }
    this.columnVisibilityChange.emit();
  }

  /**
   * On hidden change of a column search.
   */
  public onColumnSearchVisibilityChange() {
    this.columnSearchIconHidden = !this.columnSearchIconHidden;
    this.columnSearchChange.emit([]);
  }

  /**
   * Function when on sort changed emitter.
   * @param sort
   */
  public onSortChange(sort: Sort): void {
    this.sort = sort;
    this.sortChange.emit(sort);
  }

  /**
   * Page change.
   * @param page new page number
   */
  public onPageChange(page: number): void {
    this.selectedItems = [];
    this.page = page;
    this.pageChange.emit(page);
  }

  /**
   * Save table state over `TableService`.
   * @param name
   */
  public onStateSave(name: string): void {
    const columns = this.columns.filter(c => !c.hidden).map(c => c.name);
    const tableState = {
      name,
      page: this.page,
      pageSize: this.pageSize,
      sort: this.sort,
      visibleColumns: columns
    } as TableState;
    this.tableState = tableState;
    this.tableStates.push(tableState);
    this.tableService.addTableState(this.router.url, this.id, tableState);
    this.stateSave.emit(tableState);
  }

  /**
   * Update a existing state.
   * @param state
   */
  public onStateUpdate(state: TableState): void {
    const columns = this.columns.filter(c => !c.hidden).map(c => c.name);
    const tableState = {
      name: state.name,
      page: this.page,
      pageSize: this.pageSize,
      sort: this.sort,
      visibleColumns: columns
    } as TableState;
    this.tableState = tableState;
    const stateIDX = this.tableStates.indexOf(state);
    if (stateIDX > -1) {
      this.tableStates[stateIDX] = this.tableState;
    }
    this.tableService.updateTableState(this.router.url, this.id, state, this.tableState);
    this.stateUpdate.emit(tableState);
  }

  /**
   * When state was selected
   * @param state
   */
  public onStateSelect(state: TableState): void {
    this.tableState = state;
    this.tableService.setCurrentTableState(this.router.url, this.id, state);
    this.stateSelect.emit(state);
  }

  /**
   * Delete a state from the setting.
   * @param state
   */
  public onStateDelete(state: TableState): void {
    this.tableService.removeTableState(this.router.url, this.id, state);
    this.stateDelete.emit(state);
  }

  /**
   * Emit current state reset.
   */
  public onStateReset(): void {
    this.tableService.setCurrentTableState(this.router.url, this.id, undefined);
    this.stateReset.emit();
  }

  public ngOnDestroy(): void {
    this.subscriber.next();
    this.subscriber.complete();
  }
}
