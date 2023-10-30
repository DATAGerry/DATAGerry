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
import { ValidationService } from '../../../services/validation.service';

@Component({
  selector: 'cmdb-check-field-edit',
  templateUrl: './check-field-edit.component.html'
})
export class CheckFieldEditComponent extends ConfigEditBaseComponent implements OnInit {

  /**
   * Component un-subscriber.
   * @protected
   */
  protected subscriber: ReplaySubject<void> = new ReplaySubject<void>();


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
   * Value form control.
   */
  public valueControl: UntypedFormControl = new UntypedFormControl(false);

  /**
   * Helper form control.
   */
  public helperTextControl: UntypedFormControl = new UntypedFormControl('');

  private initialValue: string;
  isValid$ = true;

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

    this.disableControlOnEdit(this.nameControl);
    this.patchData(this.data, this.form);

    this.initialValue = this.nameControl.value;
  }


  public hasValidator(control: string): void {
    if (this.form.controls[control].hasValidator(Validators.required)) {

      let valid = this.form.controls[control].valid;
      this.isValid$ = this.isValid$ && valid;
    }
  }


  onInputChange(event: any, type: string) {

    console.log('onInput Change text Area')
    for (let item in this.form.controls) {
      this.hasValidator(item)
    }
    this.validationService.setIsValid(this.initialValue, this.isValid$);
    this.isValid$ = true;

  }

}
