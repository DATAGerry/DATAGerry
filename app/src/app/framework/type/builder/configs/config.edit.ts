/*
* DATAGERRY - OpenSource Enterprise CMDB
* Copyright (C) 2019 - 2021 NETHINKS GmbH
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

import { Component, EventEmitter, Input, Output } from '@angular/core';
import { CmdbType } from '../../../models/cmdb-type';
import { CmdbMode } from '../../../modes.enum';
import { Group } from '../../../../management/models/group';
import { User } from '../../../../management/models/user';
import { FormControl, FormGroup } from '@angular/forms';
import { ReplaySubject } from 'rxjs';
import { takeUntil } from 'rxjs/operators';
import { nameConvention } from '../../../../layout/directives/name.directive';

@Component({
  template: ``
})
export abstract class ConfigEditBaseComponent {


  protected abstract subscriber: ReplaySubject<void>;

  /**
   * Cmdb modes for template usage.
   */
  public MODES = CmdbMode;
  @Input() public mode: CmdbMode = CmdbMode.Create;


  @Input() public form: FormGroup;
  public abstract nameControl: FormControl;
  @Output() protected nameChange: EventEmitter<{ prev: string | undefined; curr: string | undefined }>;

  @Input() public data: any;
  @Input() public sections: Array<any>;
  @Input() public fields: Array<any> = [];

  @Input() public types: Array<CmdbType> = [];
  @Input() public groups: Array<Group> = [];
  @Input() public users: Array<User> = [];


  protected constructor() {
    this.form = new FormGroup({});
    this.nameChange = new EventEmitter<{ prev: string | undefined; curr: string | undefined }>();
  }

  protected disableControlOnEdit(control: FormControl): void {
    if (this.mode === CmdbMode.Edit) {
      control.disable({ onlySelf: false, emitEvent: false });
    }
  }

  protected validateNameLabelControl(nameControl: FormControl, labelControl: FormControl, subscriber: ReplaySubject<void>): void {
    this.disableControlOnEdit(nameControl);
    if (this.mode === CmdbMode.Create) {
      labelControl.valueChanges.pipe(takeUntil(subscriber)).subscribe((changes: string) => {
        if (!nameControl.touched) {
          nameControl.setValue(nameConvention(changes), { emitEvent: true });
        }
      });
    }
  }

  protected patchData(data: any, form: FormGroup): void {
    form.patchValue(data);
  }

  protected assignFormChanges(subscriber: ReplaySubject<void>): void {
    this.form.valueChanges.pipe(takeUntil(subscriber)).subscribe(() => {
      const formData = this.form.getRawValue();
      this.nameChange.emit({prev: this.data?.name, curr: formData?.name});
      Object.assign(this.data, formData);
    });
  }

  public calculateName(value) {
    if (this.mode !== CmdbMode.Edit) {
      this.data.name = value.replace(/ /g, '-').toLowerCase();
      this.data.name = this.data.name.replace(/[^a-z0-9 \-]/gi, '').toLowerCase();
    }
    if (!this.checkNameUniqueness()) {
      this.calculateName(this.data.name += '-1');
    }
  }

  private checkNameUniqueness() {
    const { type, name } = this.data;
    switch (type) {
      case 'section':
        return this.sections.filter(el => el.name === name).length <= 1;
      default:
        let count = 0;
        this.sections.forEach((sec) => {
          count += sec.fields.filter(el => el.name === name).length;
        });
        return count <= 1;
    }
  }
}
