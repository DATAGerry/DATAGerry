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

import { Component, OnDestroy, OnInit } from '@angular/core';
import { TypeService } from '../../../../services/type.service';
import { ConfigEditBaseComponent } from '../config.edit';
import { RenderResult } from '../../../../models/cmdb-render';
import { ObjectService } from '../../../../services/object.service';
import { CmdbType } from '../../../../models/cmdb-type';
import { CollectionParameters } from '../../../../../services/models/api-parameter';
import { takeUntil, tap } from 'rxjs/operators';
import { APIGetMultiResponse } from '../../../../../services/models/api-response';
import { Sort, SortDirection } from '../../../../../layout/table/table.types';
import { ReplaySubject } from 'rxjs';
import { ToastService } from '../../../../../layout/toast/toast.service';
import { UntypedFormControl, UntypedFormGroup, Validators } from '@angular/forms';
import { nameConvention } from '../../../../../layout/directives/name.directive';
import { ChangeDetectorRef } from '@angular/core';
import { ValidationService } from '../../../services/validation.service';
import { faL } from '@fortawesome/free-solid-svg-icons';


@Component({
  selector: 'cmdb-ref-field-edit',
  templateUrl: './ref-field-edit.component.html',
  styleUrls: ['./ref-field-edit.component.scss'],
})
export class RefFieldEditComponent extends ConfigEditBaseComponent implements OnInit, OnDestroy {

  constructor(private typeService: TypeService, private objectService: ObjectService,
    private toast: ToastService, private cd: ChangeDetectorRef,
    private validationService: ValidationService) {
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
  public nameControl: UntypedFormControl = new UntypedFormControl('', Validators.required);

  /**
   * Label form control.
   */
  public labelControl: UntypedFormControl = new UntypedFormControl('', Validators.required);

  /**
   * Type form control.
   */
  public typeControl: UntypedFormControl = new UntypedFormControl(undefined, Validators.required);

  /**
   * Summary form control.
   */
  public summaryControl: UntypedFormControl = new UntypedFormControl(undefined);

  public requiredControl: UntypedFormControl = new UntypedFormControl(false);
  /**
   * Type list for reference selection
   */
  public typesAPIResponse: APIGetMultiResponse<CmdbType>;
  public typeList: Array<CmdbType> = [];
  public filteredTypeList: CmdbType[] = [];
  public totalTypes: number = 0;


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
  public referenceGroup: UntypedFormGroup = new UntypedFormGroup({
    type_id: this.typeControl,
  });

  private initialValue: string;
  isValid$ = true;

  public ngOnInit(): void {

    this.form.addControl('required', this.requiredControl);
    this.form.addControl('name', this.nameControl);
    this.form.addControl('label', this.labelControl);
    this.form.addControl('ref_types', this.typeControl);
    this.form.addControl('summaries', this.summaryControl);

    this.disableControlOnEdit(this.nameControl);
    this.patchData(this.data, this.form);
    this.triggerAPICall();

    this.initialValue = this.nameControl.value;


    if (this.form.get('ref_types').invalid) {
      this.isValid$ = false
    }

    this.onInputChange('')

  }

  public hasValidator(control: string): void {
    if (this.form.controls[control].hasValidator(Validators.required)) {
      let valid = this.form.controls[control].valid;
      this.isValid$ = this.isValid$ && valid;
    }
  }

  public triggerAPICall() {
    this.typeLoading = true;
    this.typeService.getTypes(this.typesParams).pipe(takeUntil(this.subscriber))
      .pipe(tap(() => this.typeLoading = false))
      .subscribe(
        (apiResponse: APIGetMultiResponse<CmdbType>) => {
          this.typeList = [...apiResponse.results as Array<CmdbType>];
          this.totalTypes = apiResponse.total;
          this.typeLoading = false;
          this.prepareSummaries();
          this.cd.markForCheck();
        },
        (err) => this.toast.error(err),
        () => {
          if (this.data.ref_types) {
            this.objectService.getObjectsByType(this.data.ref_types).subscribe((res: RenderResult[]) => {
              this.objectList = res;
              this.cd.markForCheck();
            });
          }
        });
  }

  /**
   * Structure of the Summaries depending on the selected types
   * @private
   */
  private prepareSummaries() {
    if (this.data.ref_types) {
      if (!Array.isArray(this.data.ref_types)) {
        this.data.ref_types = [this.data.ref_types];
      }
      this.filteredTypeList = this.typeList.filter(type => this.data.ref_types.includes(type.public_id));
      this.data.summaries = this.data.summaries ? this.data.summaries : this.summaries;
      this.summaries = this.data.summaries;
    }
  }

  public onChange() {
    const { ref_types } = this.data;
    this.onInputChange('')
    if (Array.isArray(this.data.ref_types) && ref_types && ref_types.length === 0) {
      this.objectList = [];
      this.filteredTypeList = [];
      this.data.value = '';
    } else {
      this.objectService.getObjectsByType(ref_types).subscribe((res: RenderResult[]) => {
        this.objectList = res;
        this.prepareSummaries();
      });
    }
  }

  public summaryFieldFilter(id: number) {
    const found = this.typeList.find(s => s.public_id === id);
    return id ? found ? found.fields : [] : [];
  }

  public changeSummaryOption(type: CmdbType) {
    const nestedSummary = this.summaries.find(s => s.type_id === type.public_id);
    nestedSummary.label = type.label;
    nestedSummary.icon = type.render_meta.icon;
  }

  public changeDefault(value: any) {
    this.data.default = parseInt(value, 10);
    return this.data.default;
  }

  public addSummary() {
    if (this.filteredTypeList) {
      this.summaries.push({
        type_id: null,
        line: null,
        label: null,
        fields: [],
        icon: null,
        prefix: false,
      });
    }
  }

  public delSummary(value: any) {
    if (this.summaries.length > 0) {
      const index = this.summaries.indexOf(value, 0);
      if (index > -1) {
        this.summaries.splice(index, 1);
      }
    }
  }

  /**
   * Name converter on ng model change.
   * @param name
   */
  public onNameChange(name: string) {
    this.onInputChange(name)
    this.data.name = nameConvention(name);
  }

  onInputChange(event: any) {

    for (let item in this.form.controls) {
      this.hasValidator(item);
    }

    // this.validationService.setIsValid(this.isValid$);
    this.validationService.setIsValid(this.initialValue, this.isValid$);
    this.isValid$ = true;

  }

  /**
   * Destroy subscriptions after closed.
   */
  public ngOnDestroy(): void {
    this.subscriber.next();
    this.subscriber.complete();
  }
}
