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
import { FormControl, Validators } from '@angular/forms';

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
  public nameControl: FormControl = new FormControl('', Validators.required);

  /**
   * Label form control.
   */
  public labelControl: FormControl = new FormControl('', Validators.required);

  /**
   * Description form control.
   */
  public descriptionControl: FormControl = new FormControl('');

  /**
   * Value form control.
   */
  public valueControl: FormControl = new FormControl(false);

  /**
   * Helper form control.
   */
  public helperTextControl: FormControl = new FormControl('');

  constructor() {
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
  }

}
