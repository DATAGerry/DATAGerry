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

import { Component, Input, OnDestroy, OnInit } from '@angular/core';
import { ConfigEditBaseComponent } from '../config.edit';
import { ReplaySubject } from 'rxjs';
import { UntypedFormControl, Validators } from '@angular/forms';
import { ValidRegexValidator } from '../../../../../layout/validators/valid-regex-validator';
import { ValidationService } from '../../../services/validation.service';

@Component({
  selector: 'cmdb-textarea-edit',
  templateUrl: './textarea-edit.component.html',
  styleUrls: ['./textarea-edit.component.scss']
})
export class TextareaEditComponent extends ConfigEditBaseComponent implements OnInit, OnDestroy {

  /**
   * Component un-subscriber.
   * @protected
   */
  protected subscriber: ReplaySubject<void> = new ReplaySubject<void>();

  public requiredControl: UntypedFormControl = new UntypedFormControl(false);
  public nameControl: UntypedFormControl = new UntypedFormControl('', Validators.required);
  public labelControl: UntypedFormControl = new UntypedFormControl('', Validators.required);
  public descriptionControl: UntypedFormControl = new UntypedFormControl(undefined);
  public rowsControl: UntypedFormControl = new UntypedFormControl(5);
  public placeholderControl: UntypedFormControl = new UntypedFormControl(undefined);
  public valueControl: UntypedFormControl = new UntypedFormControl(undefined);
  public helperTextControl: UntypedFormControl = new UntypedFormControl(undefined);
  private previousNameControlValue: string = '';
  private initialValue: string;

  public constructor(private validationService: ValidationService) {
    super();
  }

  public ngOnInit(): void {
    this.form.addControl('required', this.requiredControl);
    this.form.addControl('name', this.nameControl);
    this.form.addControl('label', this.labelControl);
    this.form.addControl('description', this.descriptionControl);
    this.form.addControl('rows', this.rowsControl);
    this.form.addControl('placeholder', this.placeholderControl);
    this.form.addControl('value', this.valueControl);
    this.form.addControl('helperText', this.helperTextControl);

    this.disableControlOnEdit(this.nameControl);
    this.patchData(this.data, this.form);

    this.initialValue = this.nameControl.value;
    this.previousNameControlValue = this.nameControl.value;
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

  public ngOnDestroy(): void {
    this.subscriber.next();
    this.subscriber.complete();
  }

}
