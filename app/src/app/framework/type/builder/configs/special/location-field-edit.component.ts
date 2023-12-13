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
*
* You should have received a copy of the GNU Affero General Public License
* along with this program. If not, see <https://www.gnu.org/licenses/>.
*/

import { Component, OnDestroy, OnInit, ChangeDetectorRef } from '@angular/core';
import { UntypedFormControl, UntypedFormGroup, Validators } from '@angular/forms';
import { ReplaySubject } from 'rxjs';

import { ConfigEditBaseComponent } from '../config.edit';
import { APIGetMultiResponse } from '../../../../../services/models/api-response';
import { RenderResult } from '../../../../models/cmdb-render';
import { CmdbType } from '../../../../models/cmdb-type';
import { takeUntil, tap } from 'rxjs/operators';
import { CollectionParameters } from '../../../../../services/models/api-parameter';

import { Sort, SortDirection } from '../../../../../layout/table/table.types';
import { nameConvention } from '../../../../../layout/directives/name.directive';

import { ToastService } from '../../../../../layout/toast/toast.service';
import { ObjectService } from '../../../../services/object.service';
import { TypeService } from '../../../../services/type.service';

import { ActivatedRoute } from '@angular/router';
import { ValidationService } from '../../../services/validation.service';

@Component({
  selector: 'cmdb-location-field-edit',
  templateUrl: './location-field-edit.component.html',
  styleUrls: ['./location-field-edit.component.scss'],
})
export class LocationFieldEditComponent extends ConfigEditBaseComponent implements OnInit, OnDestroy {

  constructor(private typeService: TypeService, private objectService: ObjectService,
    private toast: ToastService, private cd: ChangeDetectorRef, private activeRoute: ActivatedRoute, private validationService: ValidationService) {
    super();
  }

  /**
   * Component un-subscriber.
   * @protected
   */
  protected subscriber: ReplaySubject<void> = new ReplaySubject<void>();

  /**
   * Name form control.
   */
  public nameControl: UntypedFormControl = new UntypedFormControl('');

  /**
   * Label form control.
   */
  public labelControl: UntypedFormControl = new UntypedFormControl('', Validators.required);

  /**
   * Type form control.
   */
  public typeControl: UntypedFormControl = new UntypedFormControl(undefined);

  /**
   * Summary form control.
   */
  public summaryControl: UntypedFormControl = new UntypedFormControl(undefined);

  /**
   * Type list for reference selection
   */
  public selectable_as_parent: boolean = false;
  public currentTypeID: number;

  /**
   * Type loading indicator.
   */
  public typeLoading: boolean = false;

  /**
   * Begin with first page.
   */
  public readonly initPage: number = 1;
  public page: number = this.initPage;

  /**
   * Filter query from the table search input.
   */
  public filter: string;

  /**
   * Default sort filter.
   */
  public sort: Sort = { name: 'public_id', order: SortDirection.DESCENDING } as Sort;

  /**
   * Nested summaries
   */
  public summaries: any[] = [];

  /**
   * Object list for default reference value
   */
  public objectList: RenderResult[];

  /**
   * Types params
   */
  public typesParams: CollectionParameters = {
    filter: undefined, limit: 0, sort: 'public_id', order: 1, page: 1
  };

  /**
   * Reference form control.
   */
  public referenceGroup: UntypedFormGroup = new UntypedFormGroup({ type_id: this.typeControl });

  public requiredControl: UntypedFormControl = new UntypedFormControl(false);


  private initialValue: string;
  isValid$ = true;

  /** LIFE CYCLE - SECTION **/
  public ngOnInit(): void {
    this.setDraggable("false");
    this.form.addControl('required', this.requiredControl);
    this.form.addControl('name', this.nameControl);
    this.form.addControl('label', this.labelControl);

    this.currentTypeID = this.activeRoute.data['_value'].type.public_id;
    this.disableControlOnEdit(this.nameControl);
    this.patchData(this.data, this.form);
    this.triggerAPICall();

    this.initialValue = this.nameControl.value;

    if (this.form.controls['label'].invalid) {
      this.isValid$ = false;
    }
  }

  public hasValidator(control: string): void {
    if (this.form.controls[control].hasValidator(Validators.required)) {

      let valid = this.form.controls[control].valid;
      this.isValid$ = this.isValid$ && valid;
    }
  }


  onInputChange(event: any) {

    for (let item in this.form.controls) {
      this.hasValidator(item)
    }
    this.validationService.setIsValid(this.initialValue, this.isValid$);
    this.isValid$ = true;

  }

  /**
   * Destroy subscriptions after closed.
   */
  public ngOnDestroy(): void {
    this.setDraggable("true");
    this.subscriber.next();
    this.subscriber.complete();
  }

  /** HELPER - SECTION **/

  public triggerAPICall() {
    this.typeLoading = true;
    this.typeService.getType(this.currentTypeID).pipe(takeUntil(this.subscriber))
      .pipe(tap(() => this.typeLoading = false))
      .subscribe(
        (apiResponse: CmdbType) => {
          this.typeLoading = false;
          this.selectable_as_parent = apiResponse.selectable_as_parent;
          console.log("getType.apiResponse: ", apiResponse);
          this.cd.markForCheck();
        },
        (err) => this.toast.error(err));
  }

  //  /**
  //  * Name converter on ng model change.
  //  * @param name
  //  */
  public onNameChange(name: string) {
    this.data.name = nameConvention(name);
  }

  public updateSelectableAsParent() {
    this.selectable_as_parent = !this.selectable_as_parent;
    this.setSelectableAsParent(this.selectable_as_parent);
    this.cd.markForCheck();
  }

  //TODO: this is just a work around and need to be set with proper angular code 
  //sets the special control location to not draggable when there is already a location present
  private setDraggable(isDraggable: string): void {
    let opacity: string = isDraggable == "true" ? "1.0" : "0.5";

    //this only works if the special control "location" is the 2nd element
    let specialControlLocation: Element = document.getElementById('specialControls').getElementsByClassName('list-group-item')[1];
    specialControlLocation.setAttribute('draggable', isDraggable);
    (specialControlLocation as HTMLElement).style.opacity = opacity;
  }

  private setSelectableAsParent(value: boolean): void {
    this.activeRoute.snapshot.data.type.selectable_as_parent = value;
  }
}


