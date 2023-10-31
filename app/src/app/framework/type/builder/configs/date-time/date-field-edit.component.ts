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
import { ConfigEditBaseComponent } from '../config.edit';
import { NgbDateAdapter, NgbDateParserFormatter } from '@ng-bootstrap/ng-bootstrap';
import { CustomDateParserFormatter, NgbStringAdapter } from '../../../../../settings/date-settings/date-settings-formatter.service';
import { ReplaySubject } from 'rxjs';
import { UntypedFormControl, Validators } from '@angular/forms';
import { takeUntil } from 'rxjs/operators';
import { DateSettingsService } from '../../../../../settings/services/date-settings.service';
import { ValidationService } from '../../../services/validation.service';

@Component({
  selector: 'cmdb-date-field-edit',
  templateUrl: './date-field-edit.component.html',
  providers: [
    {provide: NgbDateAdapter, useClass: NgbStringAdapter},
    {provide: NgbDateParserFormatter, useClass: CustomDateParserFormatter}
  ]
})
export class DateFieldEditComponent extends ConfigEditBaseComponent implements OnInit, OnDestroy {

  /**
   * Component un-subscriber.
   * @protected
   */
  protected subscriber: ReplaySubject<void> = new ReplaySubject<void>();
  public datePlaceholder = 'YYYY-MM-DD';

  public requiredControl: UntypedFormControl = new UntypedFormControl(false);
  public nameControl: UntypedFormControl = new UntypedFormControl('', Validators.required);
  public labelControl: UntypedFormControl = new UntypedFormControl('', Validators.required);
  public descriptionControl: UntypedFormControl = new UntypedFormControl(undefined);
  public valueControl: UntypedFormControl = new UntypedFormControl(undefined);
  public helperTextControl: UntypedFormControl = new UntypedFormControl(undefined);
  private previousNameControlValue: string = '';
  private initialValue: string;

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
    this.previousNameControlValue = this.nameControl.value;
  }

  public ngOnDestroy(): void {
    this.subscriber.next();
    this.subscriber.complete();
  }


  /**
   * Resets the date to null.
   */
  public resetDate() {
    this.valueControl.setValue(undefined);
    this.data.value = null;
  }


  onInputChange(event: any, type: string) {
    const isValid = type === 'name' ? this.nameControl.valid : this.labelControl.valid;
    const fieldName = 'label';
    const fieldValue = this.nameControl.value;

    this.validationService.updateValidationStatus(type, isValid, fieldName, fieldValue, this.initialValue, this.previousNameControlValue);

    if (fieldValue.length === 0) {
      this.previousNameControlValue = this.initialValue;
    } else {
      this.previousNameControlValue = fieldValue;
    }
  }

}
