/*
* dataGerry - OpenSource Enterprise CMDB
* Copyright (C) 2019 NETHINKS GmbH
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
* along with this program.  If not, see <https://www.gnu.org/licenses/>.
*/

import { Input } from '@angular/core';
import { AbstractControl, FormGroup } from '@angular/forms';
import { CmdbMode } from '../../modes.enum';
import { ToastService } from '../../../layout/services/toast.service';

// deprecated
export interface ComponentsFields {
  data: Input;
}

export class RenderField {
  private innerData: any;
  private innerValue: any;
  public MODES = CmdbMode;
  public toast: ToastService;

  @Input() public mode: CmdbMode;
  @Input() public parentFormGroup: FormGroup;

  @Input('data')
  public set data(value: any) {
    this.innerData = value;
  }

  public get data(): any {
    return this.innerData;
  }

  @Input('value')
  public set value(valueList: any) {
    this.innerValue = valueList;
  }

  public get value(): any {
    return this.innerValue;
  }

  public get controller(): AbstractControl {
    return this.parentFormGroup.get(this.data.name);
  }

  public constructor() {
  }

  public copyToClipboard() {
    const selBox = document.createElement('textarea');
    selBox.style.position = 'fixed';
    selBox.style.left = '0';
    selBox.style.top = '0';
    selBox.style.opacity = '0';
    selBox.value = this.data.value;
    document.body.appendChild(selBox);
    selBox.focus();
    selBox.select();
    document.execCommand('copy');
    document.body.removeChild(selBox);
    this.toast.show('Content was copied to clipboard');
  }

}
