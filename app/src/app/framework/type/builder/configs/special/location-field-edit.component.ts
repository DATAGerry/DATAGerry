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
import { ActivatedRoute } from '@angular/router';

import { ReplaySubject } from 'rxjs';
import { takeUntil, tap } from 'rxjs/operators';

import { ToastService } from '../../../../../layout/toast/toast.service';
import { TypeService } from '../../../../services/type.service';
import { ValidationService } from '../../../services/validation.service';

import { ConfigEditBaseComponent } from '../config.edit';
import { RenderResult } from '../../../../models/cmdb-render';
import { CmdbType } from '../../../../models/cmdb-type';
import { CollectionParameters } from '../../../../../services/models/api-parameter';
import { Sort, SortDirection } from '../../../../../layout/table/table.types';
import { nameConvention } from '../../../../../layout/directives/name.directive';


/* ------------------------------------------------------------------------------------------------------------------ */


@Component({
  selector: 'cmdb-location-field-edit',
  templateUrl: './location-field-edit.component.html',
  styleUrls: ['./location-field-edit.component.scss'],
})
export class LocationFieldEditComponent extends ConfigEditBaseComponent implements OnInit, OnDestroy {

  protected subscriber: ReplaySubject<void> = new ReplaySubject<void>();

  public nameControl: UntypedFormControl = new UntypedFormControl('', Validators.required);
  public labelControl: UntypedFormControl = new UntypedFormControl('', Validators.required);
  public typeControl: UntypedFormControl = new UntypedFormControl(undefined, Validators.required);
  public summaryControl: UntypedFormControl = new UntypedFormControl(undefined, Validators.required);

  public selectable_as_parent: boolean = true;
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

  /* ------------------------------------------------------------------------------------------------------------------ */
  /*                                                LIFE CYCLE - SECTION                                                */
  /* ------------------------------------------------------------------------------------------------------------------ */


  constructor(private typeService: TypeService,
    private toast: ToastService,
    private cd: ChangeDetectorRef,
    private activeRoute: ActivatedRoute,
    private validationService: ValidationService) {
    super();
  }



  public ngOnInit(): void {
    this.setDraggable("false");
    this.form.addControl('name', this.nameControl);
    this.form.addControl('label', this.labelControl);

    this.currentTypeID = this.activeRoute.data['_value'].type?.public_id;
    this.disableControlOnEdit(this.nameControl);
    this.patchData(this.data, this.form);
    this.triggerAPICall();

    this.validationService.initializeData('dg_location');
  }



  public ngOnDestroy(): void {
    this.setDraggable("true");
    this.subscriber.next();
    this.subscriber.complete();
  }


  /* ------------------------------------------------------------------------------------------------------------------ */
  /*                                                  HELPER - SECTION                                                  */
  /* ------------------------------------------------------------------------------------------------------------------ */

  /**
   * Retrieves the current type from db
   */
  public triggerAPICall() {
    if (this.currentTypeID) {
      this.typeLoading = true;
      this.typeService.getType(this.currentTypeID).pipe(takeUntil(this.subscriber))
        .pipe(tap(() => this.typeLoading = false))
        .subscribe(
          (apiResponse: CmdbType) => {
            this.typeLoading = false;
            this.selectable_as_parent = apiResponse.selectable_as_parent;
            this.cd.markForCheck();
          },
          (err) => this.toast.error(err));
    }
  }



  /**
   * Name converter on ng model change.
   * @param name
   */
  public onNameChange(name: string) {
    this.data.name = nameConvention(name);
  }



  //TODO: this is just a work around and need to be set with proper angular code
  /**
   * Sets the special control location to not draggable when 
   * there is already a special control location
   * 
   * @param isDraggable (boolean): Control is draggable if true, else not
   */
  private setDraggable(isDraggable: string): void {
    let opacity: string = isDraggable == "true" ? "1.0" : "0.5";

    //this only works if the special control "location" is the 2nd element
    let specialControlLocation: Element = document.getElementById('specialControls').getElementsByClassName('list-group-item')[1];
    specialControlLocation.setAttribute('draggable', isDraggable);
    (specialControlLocation as HTMLElement).style.opacity = opacity;
  }



  onInputChange(event: any, type: string) {
    const fieldValue = this.labelControl.value;
    const fieldName = 'dg_location'; // Fixed key for 'label'

    let isValid = type === 'label' ? fieldValue.length > 0 : true; // Adjust as needed

    // If type is 'label' and fieldValue.length > 0, set isValid to true
    if (type === 'label' && fieldValue.length > 0) {
      isValid = true;
    }

    // Update the validation status using the service
    this.validationService.updateValidationStatus(type, isValid, fieldName, fieldValue, fieldValue, fieldValue);
  }



  /**
   * Toggles the 'selectable_as_parent'-attribute for the type
   */
  public updateSelectableAsParent() {
    this.selectable_as_parent = !this.selectable_as_parent;
    this.setSelectableAsParent(this.selectable_as_parent);
    this.cd.markForCheck();
  }



  /**
   * Sets the selectable_as_parent in current snapshot if type exists
   * 
   * @param value (boolean): The new value for 'selectable_as_parent'
   */
  private setSelectableAsParent(value: boolean): void {
    if (this.currentTypeID) {
      this.activeRoute.snapshot.data.type.selectable_as_parent = value;
    }
  }
}


