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
import {ToastService} from '../../../../layout/services/toast.service';

@Component({
  selector: 'cmdb-object-insert',
  templateUrl: './object-insert.component.html',
  styleUrls: ['./object-insert.component.scss']
})
export class ObjectInsertComponent implements OnInit {

  public typeList: CmdbType[];
  public formType: FormGroup;
  public formFields: FormGroup;

  constructor(private typeService: TypeService, private objService: ObjectService, private toastService: ToastService) {
    this.formType = new FormGroup({
      type: new FormControl()
    });
  }

  ngOnInit() {
    this.typeService.getTypeList().subscribe((list: CmdbType[]) => {
        this.typeList = list;
      });
  }

  get type(): CmdbType {
    return this.formType ? this.formType.get('type').value : new CmdbType();
  }

  onChange(newValue) {
    const group = {};
    newValue.fields.forEach(inputTemplate => {
      group[inputTemplate.name] = new FormControl('');
    });
    this.formFields = new FormGroup(group);
  }

  onCreate(isInserted) {
    const objInstance = new CmdbObject();
    objInstance.version = '1.0.0';
    objInstance.type_id = this.type.public_id;
    objInstance.author_id = this.type.author_id;
    objInstance.active = this.type.active;

    const fieldsList: any[] = [];
    Object.entries(this.formFields.controls).forEach(
      ([key]) => {
        const text: any = document.getElementsByName(key)[0];
        fieldsList.push({name: key, value: text.value});
      }
    );
    objInstance.fields = fieldsList;

    this.objService.postAddObject(objInstance).subscribe(res => {
      console.log(res);
      this.toastService.show(isInserted, { classname: 'bg-success text-light'});
     });
  }
}
