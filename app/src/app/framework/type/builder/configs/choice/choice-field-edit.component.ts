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

import { Component, OnInit } from '@angular/core';
import { ConfigEditBaseComponent } from '../config.edit';
import { ReplaySubject } from 'rxjs';
import { UntypedFormControl, Validators } from '@angular/forms';
import { ValidRegexValidator } from '../../../../../layout/validators/valid-regex-validator';
import { ValidationService } from '../../../services/validation.service';

@Component({
  selector: 'cmdb-choice-field-edit',
  templateUrl: './choice-field-edit.component.html'
})
export class ChoiceFieldEditComponent extends ConfigEditBaseComponent implements OnInit {

  /**
   * Component un-subscriber.
   * @protected
   */
  protected subscriber: ReplaySubject<void> = new ReplaySubject<void>();

  /**
   * Required form control.
   */
  public requiredControl: UntypedFormControl = new UntypedFormControl(false);

  /**
   * Name form control.
   */
  public nameControl: UntypedFormControl = new UntypedFormControl('', Validators.required);

  /**
   * Label form control.
   */
  public labelControl: UntypedFormControl = new UntypedFormControl('', Validators.required);

  /**
   * Description form control.
   */
  public descriptionControl: UntypedFormControl = new UntypedFormControl('');

  /**
   * Helper form control.
   */
  public helperTextControl: UntypedFormControl = new UntypedFormControl('');

  /**
   * Options form control.
   */
  public optionsControl: UntypedFormControl = new UntypedFormControl([]);

  /**
   * Helper form control.
   */
  public valueControl: UntypedFormControl = new UntypedFormControl();


  /**
   * Add able options for choice selection
   */
  public options: Array<any> = [];

  private previousNameControlValue: string = '';
  private initialValue: string;

  constructor(private validationService: ValidationService) {
    super();
  }

  public ngOnInit(): void {
    this.options = this.data.options;
    if (this.options === undefined || !Array.isArray(this.options)) {
      this.options = [];
      this.options.push({
        name: `option-${ (this.options.length + 1) }`,
        label: `Option ${ (this.options.length + 1) }`
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

    this.disableControlOnEdit(this.nameControl);
    this.patchData(this.data, this.form);

    this.initialValue = this.nameControl.value;
    this.previousNameControlValue = this.nameControl.value;
  }

  /**
   * Adds a new option with default prefix
   */
  public addOption(): void {
    this.options.push({
      name: `option-${ (this.options.length + 1) }`,
      label: `Option ${ (this.options.length + 1) }`
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
