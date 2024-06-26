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
    selector: 'cmdb-check-field-edit',
    templateUrl: './check-field-edit.component.html',
    styleUrls: ['./check-field-edit.component.scss']
})
export class CheckFieldEditComponent extends ConfigEditBaseComponent implements OnInit {

    // Component un-subscriber
    protected subscriber: ReplaySubject<void> = new ReplaySubject<void>();

    public nameControl: UntypedFormControl = new UntypedFormControl('', Validators.required);
    public labelControl: UntypedFormControl = new UntypedFormControl('', Validators.required);
    public descriptionControl: UntypedFormControl = new UntypedFormControl('');
    public valueControl: UntypedFormControl = new UntypedFormControl(false);
    public helperTextControl: UntypedFormControl = new UntypedFormControl('');
    public hideFieldControl: UntypedFormControl = new UntypedFormControl(false);

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
        this.data.options = [{
            name: 'option-1',
            label: 'Option 1'
        }];

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
            "elementType": "checkbox"
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
