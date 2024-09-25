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
import { Component, OnInit } from '@angular/core';
import { UntypedFormControl, Validators } from '@angular/forms';

import { ReplaySubject } from 'rxjs';

import { ValidationService } from '../../../services/validation.service';

import { ConfigEditBaseComponent } from '../config.edit';
/* ------------------------------------------------------------------------------------------------------------------ */

@Component({
    selector: 'cmdb-choice-field-edit',
    templateUrl: './choice-field-edit.component.html',
    styleUrls: ['./choice-field-edit.component.scss']
})
export class ChoiceFieldEditComponent extends ConfigEditBaseComponent implements OnInit {

    protected subscriber: ReplaySubject<void> = new ReplaySubject<void>();

    public requiredControl: UntypedFormControl = new UntypedFormControl(false);
    public nameControl: UntypedFormControl = new UntypedFormControl('', Validators.required);
    public labelControl: UntypedFormControl = new UntypedFormControl('', Validators.required);
    public descriptionControl: UntypedFormControl = new UntypedFormControl('');
    public helperTextControl: UntypedFormControl = new UntypedFormControl('');
    public optionsControl: UntypedFormControl = new UntypedFormControl([]);
    public valueControl: UntypedFormControl = new UntypedFormControl();
    public hideFieldControl: UntypedFormControl = new UntypedFormControl(false);

    // Add able options for choice selection
    public options: Array<any> = [];

    private initialValue: string;
    isValid$: boolean = false;
    private identifierInitialValue: string;

    /* --------------------------------------------------- LIFE CYCLE --------------------------------------------------- */

    constructor(private validationService: ValidationService) {
        super();
    }


    public ngOnInit(): void {
        this.options = this.data.options;

        if (this.options === undefined || !Array.isArray(this.options)) {
            this.options = [];
            this.options.push({
                name: `option-${(this.options.length + 1)}`,
                label: `Option ${(this.options.length + 1)}`
            });
            this.data.options = this.options;
        }

        this.form.addControl('required', this.requiredControl);
        this.form.addControl('name', this.nameControl);
        this.form.addControl('label', this.labelControl);
        this.form.addControl('description', this.descriptionControl);
        this.form.addControl('helperText', this.helperTextControl);
        this.form.addControl('value', this.valueControl);
        this.form.addControl('options', this.optionsControl);
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

    /**
     * Adds a new option with default prefix
     */
    public addOption(): void {
        this.options.push({
            name: `option-${(this.options.length + 1)}`,
            label: `Option ${(this.options.length + 1)}`
        });
    }


    /**
     * Deletes a existing option.
     * @param value
     */
    public delOption(value: any): void {

        if (this.options.length > 1) {
            const index = this.options.indexOf(value, 0);

            if (index > -1) {
                this.options.splice(index, 1);
            }
        }
    }


    onInputChange(event: any, type: string) {
        this.fieldChanges$.next({
            "newValue": event,
            "inputName": type,
            "fieldName": this.nameControl.value,
            "previousName": this.initialValue,
            "elementType": "choise"
        });

        if (type == "name") {
            this.initialValue = this.nameControl.value;
        }

        setTimeout(() => {
            this.validationService.setIsValid(this.identifierInitialValue, this.isValid$);
            this.isValid$ = true;
        });
    }
}
