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
export class SearchBarTagComponent implements OnInit, OnDestroy {

  // Elements
  @ViewChild('dropdownTrigger', { static: false }) dropdownTrigger: ElementRef;

  // Events
  @Input() public tag: SearchBarTag;
  @Output() public changeEmitter: EventEmitter<SearchBarTag>;
  @Output() public deleteEmitter: EventEmitter<SearchBarTag>;

  // Forms
  public settingsFormGroup: FormGroup;

  // Subscriptions
  private settingsFormChangesSubscription: Subscription;

  public constructor() {
    this.changeEmitter = new EventEmitter<SearchBarTag>();
    this.deleteEmitter = new EventEmitter<SearchBarTag>();
    this.settingsFormChangesSubscription = new Subscription();
  }

  public ngOnInit(): void {
    this.settingsFormGroup = new FormGroup({
      searchText: new FormControl('', Validators.required),
      searchForm: new FormControl('textSearch'),
      settings: new FormGroup({
      })
    });
    this.settingsFormGroup.patchValue(this.tag);
    this.settingsFormChangesSubscription = this.settingsFormGroup.valueChanges.pipe(debounceTime(500))
      .subscribe((changes) => {
        this.tag = Object.assign(this.tag, changes);
        this.changeEmitter.emit(this.tag);
      });
  }

  public emitDelete() {
    this.deleteEmitter.emit(this.tag);
  }

  public ngOnDestroy(): void {
    this.settingsFormChangesSubscription.unsubscribe();
  }

  public get settingsControl(): FormGroup {
    return this.settingsFormGroup.get('settings') as FormGroup;
  }

  public toggleDropDown(): void {
    // Note: nasty quick hack - sry @michael - bootstrap has a known bug here - MH
    $(this.dropdownTrigger.nativeElement).click();
  }
}
