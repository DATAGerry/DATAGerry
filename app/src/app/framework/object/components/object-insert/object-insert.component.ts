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

import { Component, OnInit } from '@angular/core';
import { CmdbType } from '../../../models/cmdb-type';
import { TypeService } from '../../../services/type.service';
import { FormControl, FormGroup} from '@angular/forms';
import { CmdbObject } from '../../../models/cmdb-object';
import { ObjectService } from '../../../services/object.service';

@Component({
  selector: 'cmdb-object-insert',
  templateUrl: './object-insert.component.html',
  styleUrls: ['./object-insert.component.scss']
})
export class ObjectInsertComponent implements OnInit {

  public typeList: any[];
  public formType: FormGroup;
  public formFields: FormGroup;
  private objInstance?: CmdbObject;

  constructor(private typeService: TypeService, private objService: ObjectService) {
    this.formType = new FormGroup({
      type: new FormControl()
    });
  }

  ngOnInit() {
    this.typeService.getTypeList().subscribe((list: CmdbType[]) => {
        this.typeList = list as [];
      });
  }

  get type(): any {
    return this.formType ? this.formType.get('type') : '';
  }

  onChange(newValue) {
    const group = {};
    newValue.fields.forEach(inputTemplate => {
      group[inputTemplate.name] = new FormControl('');
    });
    this.formFields = new FormGroup(group);
  }

  onCreate() {
    this.objInstance = new CmdbObject();
    this.objInstance.version = '1.0.0';
    this.objInstance.type_id = this.type.value.public_id;
    this.objInstance.author_id = this.type.value.author_id;
    this.objInstance.active = this.type.value.active;

    const fieldsList: any[] = [];
    Object.entries(this.formFields.value).forEach(
      ([key, value]) => {
        fieldsList.push({name: key, value});
      }
    );
    this.objInstance.fields = fieldsList;

    this.objService.postObject(this.objInstance).subscribe(res => {
      console.log(res);
    });
  }
}
