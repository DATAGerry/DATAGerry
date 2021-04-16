/*
* DATAGERRY - OpenSource Enterprise CMDB
* Copyright (C) 2019 - 2021 NETHINKS GmbH
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

import { Component, EventEmitter, Input, OnDestroy, OnInit, Output, ViewChild } from '@angular/core';
import { CmdbType } from '../../../framework/models/cmdb-type';
import { ReplaySubject } from 'rxjs';
import { FormControl, FormGroup } from '@angular/forms';
import { TypeService } from '../../../framework/services/type.service';
import { takeUntil } from 'rxjs/operators';
import { APIGetMultiResponse } from '../../../services/models/api-response';
import { CollectionParameters } from '../../../services/models/api-parameter';
import { NgSelectComponent } from '@ng-select/ng-select';
import { ToastService } from '../../toast/toast.service';

@Component({
  selector: 'cmdb-type-select',
  templateUrl: './type-select.component.html',
  styleUrls: ['./type-select.component.scss']
})
export class TypeSelectComponent<T = CmdbType> implements OnInit, OnDestroy {

  /**
   * NG select component.
   */
  @ViewChild(NgSelectComponent, { static: true }) ngSelect!: NgSelectComponent;

  /**
   * Component un subscriber.
   * @private
   */
  private subscriber: ReplaySubject<void> = new ReplaySubject<void>();

  /**
   * Reactive form group.
   */
  public formGroup: FormGroup;

  @Input('formGroup')
  public set FormGroup(group: FormGroup) {
    this.formGroup = group;
    this.subscribeChanges(this.formGroup);
  }

  /**
   * Reactive form set.
   */
  public value: any;

  @Input('value')
  public set Value(value: any) {
    this.value = value;
    this.formGroup.get('type').patchValue(this.value);
  }

  /**
   * Reactive form control name
   */
  @Input() public formControlName: string = 'type';

  /**
   * Virtual scroll enabled
   */
  @Input() public virtualScroll: boolean = true;

  /**
   * Input text placeholder
   */
  @Input() public placeHolderText: string = 'Select a type';

  /**
   * Ng select label
   */
  public readonly bindLabel: string = 'label';

  /**
   * Ng select value
   */
  public readonly bindValue: string = 'public_id';

  /**
   * Ng select clearable
   */
  @Input() public clearable: boolean = true;

  /**
   * Types loading right now.
   */
  @Input() public loading: boolean = false;

  /**
   * Preload first 10 types.
   */
  @Input() public preload: boolean = true;

  /**
   * Auto load types inside component.
   */
  @Input() public autoLoad: boolean = true;

  /**
   * Ng selected item changed.
   */
  @Output() public selectedChange: EventEmitter<T> = new EventEmitter<T>();

  /**
   * New value was set.
   */
  @Output() public valueChange: EventEmitter<any> = new EventEmitter<any>();

  /**
   * Emit new loading indicator.
   * Will only send if autoLoad is true.
   */
  @Output() public loadingStatusEmitter: EventEmitter<void> = new EventEmitter<void>();

  /**
   * Already loaded types.
   */
  @Input() public types: Array<CmdbType> = [];

  /**
   * Total number of types
   */
  @Input() public totalTypes: number = 0;

  /**
   * Max number of pages.
   */
  @Input() public maxPages: number = 0;

  /**
   * Current loading page.
   */
  @Input() public currentPage: number = 0;

  constructor(private typeService: TypeService, private toast: ToastService) {
    this.formGroup = new FormGroup({
      type: new FormControl('')
    });
  }

  /**
   * Generate the api parameter.
   * @param page loading page.
   */
  public static getApiParameters(page: number = 1): CollectionParameters {
    return {
      filter: undefined, limit: 10, sort: 'public_id', order: 1, page
    } as CollectionParameters;
  }

  /**
   * Autoload on component init.
   * Triggers the autoload if no types were passed and preload is true.
   * Subscribes to the event emitters.
   */
  public ngOnInit(): void {
    if (this.types.length === 0 && this.preload) {
      this.triggerAPICall();
    }
    this.subscribeChanges(this.formGroup);
  }

  /**
   * Subscribes to form changes.
   * @param group
   */
  public subscribeChanges(group: FormGroup): void {
    group.get(this.formControlName).valueChanges.pipe(takeUntil(this.subscriber)).subscribe((change: number) => {
      this.value = change;
      this.valueChange.emit(change);
      if (this.ngSelect.selectedItems.length > 0) {
        this.selectedChange.emit(this.ngSelect.selectedItems[0].value as T);
      } else {
        this.selectedChange.emit(undefined);
      }
    });
  }


  /**
   * Increase the current page until max page and call loading the types.
   */
  public triggerAPICall(): void {
    if (this.currentPage <= this.maxPages) {
      this.currentPage += 1;
      this.loadTypesFromApi();
    }
  }

  /**
   * Loads types from the api.
   * @private
   */
  private loadTypesFromApi(): void {
    this.loading = true;
    this.typeService.getTypes(TypeSelectComponent.getApiParameters(this.currentPage))
      .pipe(takeUntil(this.subscriber)).subscribe(
      (apiResponse: APIGetMultiResponse<CmdbType>) => {
        this.types = [...this.types, ...apiResponse.results as Array<CmdbType>];
        this.totalTypes = apiResponse.total;
        this.maxPages = apiResponse.pager.total_pages;
      }, (error) => this.toast.error(error)
    ).add(() => this.loading = false);
  }

  /**
   * Triggers type loading or emits status loading when scrolled to the end.
   */
  public onScrollEnd(): void {
    if (this.autoLoad) {
      this.triggerAPICall();
    } else {
      this.loadingStatusEmitter.emit();
    }
  }

  /**
   * Un subscribe all subscriptions.
   */
  public ngOnDestroy(): void {
    this.subscriber.next();
    this.subscriber.complete();
  }

}
