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

import { Component, Input } from '@angular/core';
import { CmdbType } from '../models/cmdb-type';
import { CmdbMode } from '../modes.enum';
import { FormGroup } from '@angular/forms';
import { CmdbObject } from '../models/cmdb-object';

@Component({
  selector: 'cmdb-render',
  templateUrl: './render.component.html',
  styleUrls: ['./render.component.scss']
})
export class RenderComponent {

  private typeInstanceBack: CmdbType;
  private objectInstanceBack: CmdbObject;
  @Input() public renderForm: FormGroup = new FormGroup({});
  @Input() public fieldsGroups: FormGroup = new FormGroup({});
  @Input() public mode: CmdbMode;

  @Input('typeInstance')
  public set typeInstance(type: CmdbType) {
    if (type !== undefined) {
      this.typeInstanceBack = type;
    }
  }

  public get typeInstance(): CmdbType {
    return this.typeInstanceBack;
  }

  @Input('objectInstance')
  public set objectInstance(data: CmdbObject) {
    if (data !== undefined) {
      this.objectInstanceBack = data;
      for (const fieldData of this.objectInstance.fields) {
        if (fieldData.value !== undefined) {
          this.fieldsGroups.get(fieldData.name).setValue(fieldData.value);
        }
      }
    }
  }

  public get objectInstance(): CmdbObject {
    return this.objectInstanceBack;
  }

  public get fields() {
    return this.renderForm.get('fields');
  }

  public constructor() {
    this.renderForm = new FormGroup({});
    this.fieldsGroups = new FormGroup({});
    if (this.mode === CmdbMode.View) {
      this.fieldsGroups.disable();
    }
  }

  public getFieldByName(name: string) {
    return this.typeInstance.fields.find(field => field.name === name);
  }

}
