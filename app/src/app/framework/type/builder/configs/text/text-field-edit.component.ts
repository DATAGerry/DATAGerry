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

import { Component, EventEmitter, OnDestroy, OnInit, Output } from '@angular/core';
import { ConfigEditBaseComponent } from '../config.edit';
import { UntypedFormControl, Validators } from '@angular/forms';
import { ReplaySubject } from 'rxjs';
import { ValidRegexValidator } from '../../../../../layout/validators/valid-regex-validator';
import { ValidationService } from '../../../services/validation.service';

@Component({
  selector: 'cmdb-text-field-edit',
  templateUrl: './text-field-edit.component.html',
  styleUrls: ['./text-field-edit.component.scss']
})
export class TextFieldEditComponent extends ConfigEditBaseComponent implements OnInit, OnDestroy {

  /**
   * Component un-subscriber.
   * @protected
   */
  protected subscriber: ReplaySubject<void> = new ReplaySubject<void>();

  public requiredControl: UntypedFormControl = new UntypedFormControl(false);
  public nameControl: UntypedFormControl = new UntypedFormControl('', Validators.required);
  public labelControl: UntypedFormControl = new UntypedFormControl('', Validators.required);
  public descriptionControl: UntypedFormControl = new UntypedFormControl(undefined);
  public regexControl: UntypedFormControl = new UntypedFormControl(undefined, ValidRegexValidator);
  public placeholderControl: UntypedFormControl = new UntypedFormControl(undefined);
  public valueControl: UntypedFormControl = new UntypedFormControl(undefined);
  public helperTextControl: UntypedFormControl = new UntypedFormControl(undefined);

  private initialValue: string;
  isValid$ = true;

  constructor(private validationService: ValidationService) {
    super();
  }

  public ngOnInit(): void {
    this.form.addControl('required', this.requiredControl);
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



    // tarmah
    this.validationService.getIsValid().subscribe((isvalid) => {
      console.log("sub from src", isvalid)
    });

    this.validationService.getIsValid().subscribe((isValid) => {
      console.log('Subscription from source', isValid);
    });
    // call service to initialize the data
  }


  // onInputChange(event: any, type: string) {
  //   const isValid = type === 'name' ? this.nameControl.valid : this.labelControl.valid;
  //   const fieldName = 'label';
  //   const fieldValue = this.nameControl.value;

  //   this.validationService.updateValidationStatus(type, isValid, fieldName, fieldValue, this.initialValue, this.previousNameControlValue);

  //   if (fieldValue.length === 0) {
  //     this.previousNameControlValue = this.initialValue;
  //   } else {
  //     this.previousNameControlValue = fieldValue;
  //   }
  // }

  public hasValidator(control: string): void {
    // if !!this.form.controls[control].validator(control).hasOwnProperty(validator);
    if (this.form.controls[control].hasValidator(Validators.required)) {

      let valid = this.form.controls[control].valid;
      this.isValid$ = this.isValid$ && valid;
      // if (valid == false || valid != this.isValid$)
    }
  }

  onInputChange(event: any, type: string) {

    // tarmah
    for (let item in this.form.controls) {
      this.hasValidator(item)
    }

    // this.validationService.setIsValid(this.isValid$);
    this.validationService.setIsValid1(this.initialValue, this.isValid$);
    this.isValid$ = true;

  }

  public ngOnDestroy(): void {
    this.subscriber.next();
    this.subscriber.complete();
  }

}
