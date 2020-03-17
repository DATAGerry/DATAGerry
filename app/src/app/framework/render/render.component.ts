/*
* DATAGERRY - OpenSource Enterprise CMDB
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
import { RenderResult } from '../models/cmdb-render';

@Component({
  selector: 'cmdb-render',
  templateUrl: './render.component.html',
  styleUrls: ['./render.component.scss']
})
export class RenderComponent {

  private typeInstanceBack: CmdbType;
  private objectInstanceBack: CmdbObject;
  private renderResultBack: RenderResult = undefined;

  @Input() public renderForm: FormGroup;
  @Input() public mode: CmdbMode;
  private field: any;

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
    }
  }

  public get objectInstance(): CmdbObject {
    return this.objectInstanceBack;
  }

  @Input('renderResult')
  public set renderResult(data: RenderResult) {
    this.renderResultBack = data;
  }

  public get renderResult(): RenderResult {
    return this.renderResultBack;
  }

  @Input('currentField')
  public get currentField() {
    return this.field;
  }

  public set currentField(value) {
    this.field = value;
  }

  public get fields() {
    return this.renderForm.get('fields');
  }

  public constructor() {
    if (this.mode === CmdbMode.View) {
      this.renderForm.disable();
    }
  }

  public getFieldByName(name: string) {
    if (this.renderResult !== undefined) {
      return this.renderResult.fields.find(field => field.name === name);
    } else {
      const VALUE = 'value';
      const TYPE = 'type';
      const fields: any = this.typeInstance.fields.find(field => field.name === name);
      fields.default = fields[VALUE];

      switch (fields[TYPE]) {
        case 'date': {
          if (fields.value instanceof Object) {
            const temp = fields.value;
            fields.default = temp.year + '-' + temp.month + '-' + temp.day;
            fields.value = fields.default;
          }
          break;
        }
        case 'ref': {
          fields.default = parseInt(fields.default, 10);
          fields.value = fields.default;
          break;
        }
        default: {
          break;
        }
      }

      return fields;
    }
  }

  public getValueByName(name: string) {
    if (this.renderResult !== undefined) {
      const fieldFound = this.renderResult.fields.find(field => field.name === name);
      if (fieldFound === undefined) {
        return {};
      }
      return fieldFound.value;
    } else if (this.objectInstance !== undefined) {
      const fieldFound = this.objectInstance.fields.find(field => field.name === name);
      if (fieldFound === undefined) {
        return {};
      }
      return fieldFound.value;
    }
  }

}
