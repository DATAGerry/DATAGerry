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
import { takeUntil } from 'rxjs/operators';

import { NgbDateAdapter, NgbDateParserFormatter } from '@ng-bootstrap/ng-bootstrap';

import { DateSettingsService } from '../../../../../settings/services/date-settings.service';
import { ValidationService } from '../../../services/validation.service';

import { ConfigEditBaseComponent } from '../config.edit';
import { CustomDateParserFormatter, NgbStringAdapter } from '../../../../../settings/date-settings/date-settings-formatter.service';
/* ------------------------------------------------------------------------------------------------------------------ */

@Component({
  selector: 'cmdb-date-field-edit',
  templateUrl: './date-field-edit.component.html',
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

  private initialValue: string;
  isValid$ = true;


/* --------------------------------------------------- LIFE CYCLE --------------------------------------------------- */
    constructor(private dateSettingsService: DateSettingsService, private validationService: ValidationService) {
        super();
    }


    public ngOnInit(): void {
        this.dateSettingsService.getDateSettings().pipe(takeUntil(this.subscriber)).subscribe((dateSettings: any) => {
            this.datePlaceholder = dateSettings.date_format;
        });

        this.form.addControl('required', this.requiredControl);
        this.form.addControl('name', this.nameControl);
        this.form.addControl('label', this.labelControl);
        this.form.addControl('description', this.descriptionControl);
        this.form.addControl('value', this.valueControl);
        this.form.addControl('helperText', this.helperTextControl);

        this.disableControlOnEdit(this.nameControl);
        this.patchData(this.data, this.form);

        this.initialValue = this.nameControl.value;
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
            "inputName":type,
            "fieldName": this.nameControl.value
        });

        for (let item in this.form.controls) {
            this.hasValidator(item)
        }

        this.validationService.setIsValid(this.initialValue, this.isValid$);
        this.isValid$ = true;
    }


    /**
     * Resets the date to null.
     */
    public resetDate() {
        this.valueControl.setValue(undefined);
        this.data.value = null;
    }
}
