/*
* DATAGERRY - OpenSource Enterprise CMDB
* Copyright (C) 2024 becon GmbH
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
import { takeUntil, tap } from 'rxjs/operators';

import { TypeService } from '../../../../services/type.service';
import { ObjectService } from '../../../../services/object.service';
import { ToastService } from '../../../../../layout/toast/toast.service';
import { ValidationService } from '../../../services/validation.service';

import { ConfigEditBaseComponent } from '../config.edit';
import { RenderResult } from '../../../../models/cmdb-render';
import { CmdbType } from '../../../../models/cmdb-type';
import { CollectionParameters } from '../../../../../services/models/api-parameter';
import { APIGetMultiResponse } from '../../../../../services/models/api-response';
import { Sort, SortDirection } from '../../../../../layout/table/table.types';
import { nameConvention } from '../../../../../layout/directives/name.directive';
/* ------------------------------------------------------------------------------------------------------------------ */

@Component({
    selector: 'cmdb-ref-field-edit',
    templateUrl: './ref-field-edit.component.html',
    styleUrls: ['./ref-field-edit.component.scss'],
})
export class RefFieldEditComponent extends ConfigEditBaseComponent implements OnInit, OnDestroy {

    protected subscriber: ReplaySubject<void> = new ReplaySubject<void>();

    public nameControl: UntypedFormControl = new UntypedFormControl('', Validators.required);
    public labelControl: UntypedFormControl = new UntypedFormControl('', Validators.required);
    public typeControl: UntypedFormControl = new UntypedFormControl(undefined, Validators.required);
    public summaryControl: UntypedFormControl = new UntypedFormControl(undefined);
    public requiredControl: UntypedFormControl = new UntypedFormControl(false);

    // Type list for reference selection
    public typesAPIResponse: APIGetMultiResponse<CmdbType>;
    public typeList: Array<CmdbType> = [];
    public filteredTypeList: CmdbType[] = [];
    public totalTypes: number = 0;

    //type loading indicator
    public typeLoading: boolean = false;

    public readonly initPage: number = 1;
    public page: number = this.initPage;

    // Filter query from the table search input.
    public filter: string;

    public sort: Sort = { name: 'public_id', order: SortDirection.DESCENDING } as Sort;

    // Nested summaries
    public summaries: any[] = [];

    // Object list for default reference value
    public objectList: RenderResult[];

    public typesParams: CollectionParameters = {
        filter: undefined, limit: 0, sort: 'public_id', order: 1, page: 1
    };

    // Reference form control
    public referenceGroup: UntypedFormGroup = new UntypedFormGroup({
        type_id: this.typeControl,
    });

    private initialValue: string;
    private identifierInitialValue: string;
    isValid$ = true;

    /* ------------------------------------------------------------------------------------------------------------------ */
    /*                                                     LIFE CYCLE                                                     */
    /* ------------------------------------------------------------------------------------------------------------------ */

    constructor(
        private typeService: TypeService,
        private objectService: ObjectService,
        private toast: ToastService,
        private cd: ChangeDetectorRef,
        private validationService: ValidationService
    ) {
        super();
    }


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
        this.identifierInitialValue = this.nameControl.value

        if (this.form.get('ref_types').invalid) {
            this.isValid$ = false
        }

        setTimeout(() => {
            this.onInputChange();
        }, 0);
    }


    public ngOnDestroy(): void {
        this.subscriber.next();
        this.subscriber.complete();
    }

    /* ----------------------------------------------- ON_CHANGES SECTION ----------------------------------------------- */

    /**
     * Feed the subject with changes to field properties
     * @param event the new value of the field
     * @param type the type of the field
     */
    onRefInputChange(event: any, type: string) {
        this.fieldChanges$.next({
            "newValue": event,
            "inputName": type,
            "fieldName": this.nameControl.value,
            "previousName": this.initialValue,
            "elementType": "ref"
        });

        if (type == "name") {
            this.initialValue = this.nameControl.value;
        }
    }


    public onChange() {
        const { ref_types } = this.data;
        this.data.ref_types = this.form.controls.ref_types.value;

        this.onInputChange();

        if (Array.isArray(this.data.ref_types) && ref_types && ref_types.length === 0) {
            this.objectList = [];
            this.filteredTypeList = [];
            this.data.value = '';
        } else {
            this.objectService.getObjectsByType(this.data.ref_types).subscribe((res: RenderResult[]) => {
                this.objectList = res;
                this.prepareSummaries();
            });
        }

        this.filterSummaries();
    }

    /**
     * Filters the summaries based on the reference types available in the data.
     * Only includes summaries where the type_id exists in the ref_types.
    */
    private filterSummaries() {
        if (this.data.ref_types) {
            this.summaries = this.summaries.filter(summary =>
                this.data.ref_types.includes(summary.type_id)
            );
        }
    }


    public changeDefault(value: any) {
        this.data.default = parseInt(value, 10);

        return this.data.default;
    }


    /**
     * Name converter on ng model change.
     * @param name
     */
    public onNameChange(name: string) {
        this.onInputChange();
        this.data.name = nameConvention(name);
    }


    onInputChange() {
        for (let item in this.form.controls) {
            this.hasValidator(item);
        }

        this.validationService.setIsValid(this.identifierInitialValue, this.isValid$);
        this.isValid$ = true;
    }

    /* --------------------------------------------------- API SECTION -------------------------------------------------- */

    public triggerAPICall() {
        this.typeLoading = true;

        this.typeService.getTypes(this.typesParams).pipe(takeUntil(this.subscriber))
            .pipe(tap(() => this.typeLoading = false))
            .subscribe({
                next: (apiResponse: APIGetMultiResponse<CmdbType>) => {
                    this.typeList = [...apiResponse.results as Array<CmdbType>];
                    this.totalTypes = apiResponse.total;
                    this.prepareSummaries();
                    this.cd.markForCheck();
                },
                error: (err) => this.toast.error(err),
                complete: () => {
                    if (this.data.ref_types) {
                        this.objectService.getObjectsByType(this.data.ref_types).subscribe((res: RenderResult[]) => {
                            this.objectList = res;
                            this.cd.markForCheck();
                        });
                    }
                }
            });
    }

    /* ------------------------------------------------- SUMMARY SECTION ------------------------------------------------ */

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
        this.cd.detectChanges()
    }


    public summaryFieldFilter(id: number) {
        const found = this.typeList.find(s => s.public_id === id);

        return id ? found ? found.fields : [] : [];
    }


    /**
     * Handles the change event for the ng-select component.
     * Updates the corresponding summary item with the selected type's label and icon.
     * @param type - The selected type object containing the public_id, label, and render_meta.icon.
    */
    public changeSummaryOption(type: CmdbType, summary: any) {

        if (!type) {
            summary.label = '';
            summary.line = '';
            summary.fields = [];
            return;
        }
        const nestedSummary = this.summaries.find(s => s.type_id === type.public_id);
        if (nestedSummary) {
            nestedSummary.label = type.label;
            nestedSummary.icon = type.render_meta.icon;
        } else {
            console.warn('No matching summary found for type_id:', type.public_id);
        }
    }


    /* ------------------------------------------------- HELPER SECTION ------------------------------------------------- */

    public hasValidator(control: string): void {
        if (this.form.controls[control].hasValidator(Validators.required)) {
            let valid = this.form.controls[control].valid;
            this.isValid$ = this.isValid$ && valid;
        }
    }
}
