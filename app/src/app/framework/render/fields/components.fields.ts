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
import { FormControl, FormGroup } from '@angular/forms';

// deprecated
export interface ComponentsFields {
  data: Input;
}

export class RenderField {
  private innerData: any;

  @Input() parentFormGroup: FormGroup;

  @Input('data')
  public set data(value: any) {
    this.innerData = value;
    this.parentFormGroup.addControl(
      this.data.name, new FormControl('')
    );
  }

  public get data(): any {
    return this.innerData;
  }

  public constructor() {
    this.parentFormGroup = new FormGroup({});
  }

}
