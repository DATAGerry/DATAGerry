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
  Component, ComponentFactoryResolver, ContentChild,
  ElementRef,
  EventEmitter, Injector,
  Input,
  OnDestroy,
  OnInit,
  Output, TemplateRef,
  ViewChild,
  ViewEncapsulation
} from '@angular/core';
import { ReplaySubject } from 'rxjs';
import { Column, Sort } from './models';
import { takeUntil } from 'rxjs/operators';

@Component({
  selector: 'cmdb-table',
  templateUrl: './table.component.html',
  styleUrls: ['./table.component.scss'],
  encapsulation: ViewEncapsulation.None,
  changeDetection: ChangeDetectionStrategy.Default,
})
export class TableComponent<T> implements OnInit, OnDestroy {

  private subscriber: ReplaySubject<void> = new ReplaySubject<void>();

  @Input() public columns: Array<Column> = [];
  @Input() public items: Array<T> = [];
  @Input() public totalItems: number = 0;

  /**
   * Is row selected enabled.
   */
  @Input() public selection: boolean = false;

  /**
   * Selected rows.
   */
  @Input() public selected: Array<T> = [];

  // SORT
  @Input() public sortAble: boolean = true;

  @Input() public infoEnabled: boolean = true;
  @Input() public pageLengthEnabled: boolean = true;
  @Input() public searchEnabled: boolean = true;
  @Input() public paginationEnabled: boolean = true;

  @Output() public sortChange: EventEmitter<Sort> = new EventEmitter<Sort>();
  @Output() public pageSizeChange: EventEmitter<number> = new EventEmitter<number>();
  @Output() public pageChange: EventEmitter<number> = new EventEmitter<number>();
  @Output() public searchChange: EventEmitter<string> = new EventEmitter<string>();
  @Output() public selectionChange: EventEmitter<Array<T>> = new EventEmitter<Array<T>>();


  constructor() {

  }

  public ngOnInit(): void {
    this.pageSizeChange.asObservable().pipe(takeUntil(this.subscriber)).subscribe((size: number) => {
      console.log(`[TableEvent] Page size changed to: ${ size }`);
    });
    this.pageChange.asObservable().pipe(takeUntil(this.subscriber)).subscribe((page: number) => {
      console.log(`[TableEvent] Page changed to: ${ page }`);
    });
    this.searchChange.asObservable().pipe(takeUntil(this.subscriber)).subscribe((search: string) => {
      console.log(`[TableEvent] Search input changed to: ${ search }`);
    });
    this.selectionChange.asObservable().pipe(takeUntil(this.subscriber)).subscribe((selected: Array<T>) => {
      console.log(`[TableEvent] Selected rows changed to: ${ selected }`);
    });
  }

  /**
   * Select a row
   */
  public toggleRowSelection(item: T, event: any): void {
    const checked = event.currentTarget.checked;
    if (checked) {
      this.selected.push(item);
    } else {
      const idx = this.selected.indexOf(item);
      if (idx !== -1) {
        this.selected.splice(idx, 1);
      }
    }
    this.selectionChange.emit(this.selected);
  }

  public ngOnDestroy(): void {
    this.subscriber.next();
    this.subscriber.complete();
  }


}
