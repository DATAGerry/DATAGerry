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
* along with this program.  If not, see <https://www.gnu.org/licenses/>.
*/

import { Component, ElementRef, EventEmitter, Input, OnDestroy, OnInit, Output, ViewChild } from '@angular/core';
import { SearchBarTag, SearchBarTagSettings } from './search-bar-tag';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { Subscription } from 'rxjs';
import { debounceTime } from 'rxjs/operators';

import * as $ from 'jquery';

@Component({
  selector: 'cmdb-search-bar-tags',
  templateUrl: './search-bar-tag.component.html',
  styleUrls: ['./search-bar-tag.component.scss']
})
export class SearchBarTagComponent implements OnDestroy {

  // Elements
  @ViewChild('dropdownTrigger') dropdownTrigger: ElementRef;

  // Events
  @Input() public tag: SearchBarTag;
  @Output() public changeEmitter: EventEmitter<SearchBarTag>;
  @Output() public deleteEmitter: EventEmitter<SearchBarTag>;


  public constructor() {
    /**
     * Default constructor
     * Change form is deactivated
     */
    this.changeEmitter = new EventEmitter<SearchBarTag>();
    this.deleteEmitter = new EventEmitter<SearchBarTag>();
    // this.settingsFormChangesSubscription = new Subscription();
  }


  public emitDelete() {
    this.deleteEmitter.emit(this.tag);
  }

  public ngOnDestroy(): void {
    // this.settingsFormChangesSubscription.unsubscribe();
  }
}
