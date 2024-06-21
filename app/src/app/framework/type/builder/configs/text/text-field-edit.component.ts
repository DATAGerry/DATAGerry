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
import { Component, OnDestroy, OnInit } from '@angular/core';
import { UntypedFormControl, Validators } from '@angular/forms';

import { ReplaySubject } from 'rxjs';

import { ValidationService } from '../../../services/validation.service';

import { ValidRegexValidator } from '../../../../../layout/validators/valid-regex-validator';

import { ConfigEditBaseComponent } from '../config.edit';
/* ------------------------------------------------------------------------------------------------------------------ */

@Component({
    selector: 'cmdb-text-field-edit',
    templateUrl: './text-field-edit.component.html',
    styleUrls: ['./text-field-edit.component.scss']
})
export class TextFieldEditComponent extends ConfigEditBaseComponent implements OnInit, OnDestroy {

    protected subscriber: ReplaySubject<void> = new ReplaySubject<void>();

    public requiredControl: UntypedFormControl = new UntypedFormControl(false);
    public hideFieldControl: UntypedFormControl = new UntypedFormControl(false);
    public nameControl: UntypedFormControl = new UntypedFormControl('', Validators.required);
    public labelControl: UntypedFormControl = new UntypedFormControl('', Validators.required);
    public descriptionControl: UntypedFormControl = new UntypedFormControl(undefined);
    public regexControl: UntypedFormControl = new UntypedFormControl(undefined, ValidRegexValidator);
    public placeholderControl: UntypedFormControl = new UntypedFormControl(undefined);
    public valueControl: UntypedFormControl = new UntypedFormControl(undefined);
    public helperTextControl: UntypedFormControl = new UntypedFormControl(undefined);

    private initialValue: string;
    isValid$ = true;

    private identifierInitialValue: string;

    /* ------------------------------------------------------------------------------------------------------------------ */
    /*                                                     LIFE CYCLE                                                     */
    /* ------------------------------------------------------------------------------------------------------------------ */

    constructor(private validationService: ValidationService) {
        super();
    }


    public ngOnInit(): void {
        this.form.addControl('required', this.requiredControl);
        this.form.addControl('hideField', this.hideFieldControl);
        this.form.addControl('name', this.nameControl);
        this.form.addControl('label', this.labelControl);
        this.form.addControl('description', this.descriptionControl);
        this.form.addControl('regex', this.regexControl);
        this.form.addControl('placeholder', this.placeholderControl);
        this.form.addControl('value', this.valueControl);
        this.form.addControl('helperText', this.helperTextControl);

        this.disableControlOnEdit(this.nameControl);
        this.patchData(this.data, this.form);

        this.initialValue = this.nameControl.value;
        this.identifierInitialValue = this.nameControl.value;

        if (this.hiddenStatus) {
            this.hideFieldControl.setValue(true);
        }

    }


    public ngOnDestroy(): void {
        this.subscriber.next();
        this.subscriber.complete();
    }

    /* ---------------------------------------------------- FUNCTIONS --------------------------------------------------- */

    public hasValidator(control: string): void {
        if (this.form.controls[control].hasValidator(Validators.required)) {
            let valid = this.form.controls[control].valid;
            this.isValid$ = this.isValid$ && valid;
        }
    }


    onInputChange(event: any, type: string) {
        this.fieldChanges$.next({
            "newValue": event,
            "inputName": type,
            "fieldName": this.nameControl.value,
            "previousName": this.initialValue,
            "elementType": "text"
        });

        if (type == "name") {
            this.initialValue = this.nameControl.value;
        }

        for (let item in this.form.controls) {
            this.hasValidator(item);
        }

        this.validationService.setIsValid(this.identifierInitialValue, this.isValid$);
        this.isValid$ = true;
    }

}
