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

import {Component, Input} from '@angular/core';
import {CmdbObject} from '../../../models/cmdb-object';
import {ApiCallService} from '../../../../services/api-call.service';
import {ObjectService} from '../../../services/object.service';
import {FormGroup} from '@angular/forms';

@Component({
  selector: 'cmdb-object-fields-view',
  templateUrl: './object-fields-view.component.html',
  styleUrls: ['./object-fields-view.component.scss']
})
export class ObjectFieldsViewComponent {

  @Input() objectInstance: any;
  @Input() isDisable: boolean;
  public formFields: FormGroup = new FormGroup({});

  constructor(private api: ApiCallService, private objService: ObjectService) {  }

  public revert() {
    console.log('revert');
  }

  public update(instance: any) {

    const updateInstance = new CmdbObject();
    updateInstance.public_id = Number(instance.object_id);
    updateInstance.type_id = instance.type_id;
    updateInstance.version = '1.0.0';
    updateInstance.creation_time = instance.object_creation_time;
    updateInstance.author_id = instance.author_id;
    updateInstance.active = instance.type_active;

    const fieldsList: any[] = [];
    for (const field of instance.obj_fields) {
      const text: any = document.getElementsByName(field.name)[0];
      fieldsList.push({name: field.name, value: text.value });
    }

    updateInstance.fields = fieldsList;
    console.log(updateInstance);
    this.objService.postUpdateObject(updateInstance).subscribe(res => {
      console.log(res);
    });
  }

}
