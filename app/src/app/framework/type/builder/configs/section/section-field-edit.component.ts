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
* along with this program.  If not, see <https://www.gnu.org/licenses/>.
*/
import { Component, OnDestroy, OnInit } from '@angular/core';
import { UntypedFormControl, Validators } from '@angular/forms';

import { ReplaySubject } from 'rxjs';

import { ValidationService } from '../../../services/validation.service';

import { ConfigEditBaseComponent } from '../config.edit';
import { SectionIdentifierService } from '../../../services/SectionIdentifierService.service';
/* ------------------------------------------------------------------------------------------------------------------ */

@Component({
    selector: 'cmdb-section-field-edit',
    templateUrl: './section-field-edit.component.html'
})
export class SectionFieldEditComponent extends ConfigEditBaseComponent implements OnInit, OnDestroy {

    protected subscriber: ReplaySubject<void> = new ReplaySubject<void>();

    public nameControl: UntypedFormControl = new UntypedFormControl('', Validators.required);
    public labelControl: UntypedFormControl = new UntypedFormControl('', Validators.required);

    private initialValue: string;
    private identifierInitialValue: string;
    isValid$ = true;
    public currentValue: string;
    public isIdentifierValid: boolean = true;

    /* ------------------------------------------------------------------------------------------------------------------ */
    /*                                                     LIFE CYCLE                                                     */
    /* ------------------------------------------------------------------------------------------------------------------ */

    public constructor(private validationService: ValidationService, private sectionIdentifier: SectionIdentifierService) {
        super();
    }


    public ngOnInit(): void {
        this.form.addControl('name', this.nameControl);
        this.form.addControl('label', this.labelControl);

        this.disableControlOnEdit(this.nameControl);
        this.disableControlsOnGlobal(this.nameControl);
        this.disableControlsOnGlobal(this.labelControl);
        this.patchData(this.data, this.form);
        this.initialValue = this.nameControl.value;
        this.identifierInitialValue = this.nameControl.value;
        this.currentValue = this.identifierInitialValue;
    }

    public ngOnDestroy(): void {
        this.subscriber.next();
        this.subscriber.complete();
    }

    /* ------------------------------------------------- HELPER METHODS ------------------------------------------------- */

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
            "elementType": "section",
        });

        if (type === "name") {
            const newName = this.nameControl.value;
            this.initialValue = newName;
        }

        for (let item in this.form.controls) {
            this.hasValidator(item);
        }

        this.validationService.setIsValid(this.identifierInitialValue, this.isValid$);
        this.isValid$ = true;

        this.updateSectionValue(this.nameControl.value)
    }


    updateSectionValue(newValue: string): void {
        const isValid = this.sectionIdentifier.updateSection(this.identifierInitialValue, newValue);
        if (!isValid) {
            this.isIdentifierValid = false
        } else {
            this.currentValue = newValue;
            this.isIdentifierValid = true;
        }
    }
}
