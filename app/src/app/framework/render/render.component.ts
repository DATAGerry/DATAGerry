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

import { Component, EventEmitter, Input, Output } from '@angular/core';
import { CmdbType } from '../models/cmdb-type';
import { CmdbMode } from '../modes.enum';
import { FormControl, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'cmdb-render',
  templateUrl: './render.component.html',
  styleUrls: ['./render.component.scss']
})
export class RenderComponent {

  private typeInstanceBack: CmdbType;
  public renderForm: FormGroup;
  public fieldsGroups: FormGroup;

  @Input() public mode: CmdbMode;
  @Output() parentSubmit = new EventEmitter<any>();

  @Input('typeInstance')
  public set typeInstance(type: CmdbType) {
    this.typeInstanceBack = type;
    for (const section of this.typeInstance.render_meta.sections) {

      for (const field of this.typeInstance.fields) {
        let fieldControl = new FormControl('');
        if (field.required) {
          fieldControl = new FormControl('', Validators.required);
        }
        this.fieldsGroups.addControl(
          field.name, fieldControl
        );
      }
    }
  }

  public get typeInstance(): CmdbType {
    return this.typeInstanceBack;
  }

  public constructor() {
    this.fieldsGroups = new FormGroup({});
    this.renderForm = new FormGroup({
      active: new FormControl(true),
      fields: this.fieldsGroups
    });
  }

  public get fields() {
    return this.renderForm.get('fields');
  }

  public onSubmit() {
    this.parentSubmit.emit();
  }

  public getFieldByName(name: string) {
    return this.typeInstance.fields.find(field => field.name === name);
  }

}
