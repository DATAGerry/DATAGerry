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
import { Component, ElementRef, OnDestroy, OnInit, ViewChild } from '@angular/core';
import { UntypedFormControl, Validators } from '@angular/forms';

import { ReplaySubject } from 'rxjs';

import { NgbDateAdapter, NgbDateParserFormatter } from '@ng-bootstrap/ng-bootstrap';

import { ValidationService } from '../../../services/validation.service';

import { CustomDateParserFormatter, NgbStringAdapter } from '../../../../../settings/date-settings/date-settings-formatter.service';

import { ConfigEditBaseComponent } from '../config.edit';
/* ------------------------------------------------------------------------------------------------------------------ */

@Component({
    selector: 'cmdb-date-field-edit',
    templateUrl: './date-field-edit.component.html',
    styleUrls: ['./date-field-edit.component.scss'],
    providers: [
        { provide: NgbDateAdapter, useClass: NgbStringAdapter },
        { provide: NgbDateParserFormatter, useClass: CustomDateParserFormatter }
    ]
})
export class DateFieldEditComponent extends ConfigEditBaseComponent implements OnInit, OnDestroy {

    protected subscriber: ReplaySubject<void> = new ReplaySubject<void>();
    public datePlaceholder = 'YYYY-MM-DD';

    public requiredControl: UntypedFormControl = new UntypedFormControl(false);
    public nameControl: UntypedFormControl = new UntypedFormControl('', Validators.required);
    public labelControl: UntypedFormControl = new UntypedFormControl('', Validators.required);
    public descriptionControl: UntypedFormControl = new UntypedFormControl(undefined);
    public valueControl: UntypedFormControl = new UntypedFormControl(undefined);
    public helperTextControl: UntypedFormControl = new UntypedFormControl(undefined);
    public hideFieldControl: UntypedFormControl = new UntypedFormControl(false);

    private initialValue: string;
    private identifierInitialValue: string;
    isValid$: boolean = false;
    date: Date;

    @ViewChild('dateInputVisible') dateInputVisible: ElementRef<HTMLInputElement>;
    @ViewChild('dateInputHidden') dateInputHidden: ElementRef<HTMLInputElement>;
    isDatePickerVisible = true;

    /* ------------------------------------------------------------------------------------------------------------------ */
    /*                                                     LIFE CYCLE                                                     */
    /* ------------------------------------------------------------------------------------------------------------------ */

    constructor(private validationService: ValidationService) {
        super();
    }


    public ngOnInit(): void {
        this.form.addControl('required', this.requiredControl);
        this.form.addControl('name', this.nameControl);
        this.form.addControl('label', this.labelControl);
        this.form.addControl('description', this.descriptionControl);
        this.form.addControl('value', this.valueControl);
        this.form.addControl('helperText', this.helperTextControl);
        this.form.addControl('hideField', this.hideFieldControl);

        this.disableControlOnEdit(this.nameControl);
        this.patchData(this.data, this.form);

        this.initialValue = this.nameControl.value;
        this.identifierInitialValue = this.nameControl.value;

        if (this.hiddenStatus) {
            this.hideFieldControl.setValue(true);
        }


        // Initialize only once
        if (!this.identifierInitialValue) {
            this.identifierInitialValue = this.nameControl.value;
        }

        this.isValid$ = this.form.valid;

        // Subscribe to form status changes and update isValid$ based on form validity
        this.form.statusChanges.subscribe(() => {
            this.isValid$ = this.form.valid;
        });
    }


    public ngOnDestroy(): void {
        //   When moving a field, if the identifier changes, delete the old one and add the new one.
        if (this.identifierInitialValue != this.nameControl.value) {
            this.validationService.updateFieldValidityOnDeletion(this.identifierInitialValue);
        }
        this.subscriber.next();
        this.subscriber.complete();
    }

    /* ---------------------------------------------------- FUNCTIONS --------------------------------------------------- */



    onInputChange(event: any, type: string) {
        this.fieldChanges$.next({
            "newValue": event,
            "inputName": type,
            "fieldName": this.nameControl.value,
            "previousName": this.initialValue,
            "elementType": "date"
        });

        if (type == "name") {
            this.initialValue = this.nameControl.value;
        }

        setTimeout(() => {
            this.validationService.setIsValid(this.identifierInitialValue, this.isValid$);
            this.isValid$ = true;
        });
    }


    /**
     * Toggles the input type between 'date' and 'text' on double click.
     */
    onDblClick(event: MouseEvent) {
        const inputElement = event.target as HTMLInputElement;
        if (inputElement.type === 'date') {
            inputElement.type = 'text';

            setTimeout(() => {
                inputElement.select();
            });
        }
    }


    /**
     * Changes the input type back to 'date' when the input element loses focus,
     * if the current type is 'text'.
     */
    onFocusOut(event: FocusEvent) {
        const inputElement = event.target as HTMLInputElement;
        if (inputElement.type === 'text') {
            inputElement.type = 'date';
        }
    }


    /**
     * Resets the date to null.
     */
    public resetDate() {
        this.valueControl.setValue(undefined);
        this.data.value = null;
    }
}
