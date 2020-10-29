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

import { Component, EventEmitter, Input, OnDestroy, OnInit, Output } from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';
import { debounceTime, takeUntil } from 'rxjs/operators';
import { ReplaySubject } from 'rxjs';

@Component({
  // tslint:disable-next-line:component-selector
  selector: 'table-search',
  templateUrl: './table-search.component.html',
  styleUrls: ['./table-search.component.scss']
})
export class TableSearchComponent implements OnInit, OnDestroy {

  /**
   * Component un-subscriber.
   * @private
   */
  private subscriber: ReplaySubject<void> = new ReplaySubject<void>();

  /**
   * Search input form group.
   */
  public form: FormGroup;

  /**
   * Default time slot for change emits.
   * @private
   */
  private readonly defaultDebounceTime: number = 500;

  /**
   * Time debounce for search change emits.
   */
  public debounceTime: number = this.defaultDebounceTime;

  /**
   * DebounceTime setter.
   * @param time Debounce time in ms.
   */
  @Input('debounceTime')
  public set DebounceTime(time: number) {
    this.debounceTime = time || this.defaultDebounceTime;
  }

  /**
   * Event emitter when the search input changed.
   */
  @Output() public searchChange: EventEmitter<string> = new EventEmitter<string>();

  /**
   * Constructor of `TableSearchComponent`.
   */
  constructor() {
    this.form = new FormGroup({
      search: new FormControl()
    });
  }

  /**
   * OnInit of `TableSearchComponent`.
   * Auto subscribes to search input control values changes.
   * Emits changes to searchChange EventEmitter.
   */
  public ngOnInit(): void {
    this.search.valueChanges.pipe(takeUntil(this.subscriber)).pipe(debounceTime(this.debounceTime))
      .subscribe(change => this.searchChange.emit(change));
  }

  /**
   * Get the search form control.
   */
  public get search(): FormControl {
    return this.form.get('search') as FormControl;
  }

  /**
   * OnDestroy of `TableSearchComponent`.
   * Sends complete call to the component subscriber.
   */
  public ngOnDestroy(): void {
    this.subscriber.next();
    this.subscriber.complete();
  }

}
