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

import {Component, Input, OnChanges, OnInit, SimpleChanges} from '@angular/core';
import {CmdbObject} from '../../../models/cmdb-object';
import {ApiCallService} from '../../../../services/api-call.service';
import {ObjectService} from '../../../services/object.service';
import {CmdbType} from '../../../models/cmdb-type';

@Component({
  selector: 'cmdb-object-fields-view',
  templateUrl: './object-fields-view.component.html',
  styleUrls: ['./object-fields-view.component.scss']
})
export class ObjectFieldsViewComponent implements OnInit, OnChanges {

  @Input() objectInstance: any;
  @Input() isDisable: boolean;
  public currentType: CmdbType;

  constructor(private api: ApiCallService, private objService: ObjectService) {  }

  ngOnInit(): void { }

  ngOnChanges(changes: SimpleChanges) {
    if (changes.objectInstance) {
      const variableChange: any = changes.objectInstance;
      if (variableChange.currentValue !== undefined) {
        console.log(variableChange);
        this.api.callGetRoute<any>('type/' + variableChange.currentValue.type_id)
          .subscribe(data => this.currentType = data);
      }
    }
  }

  public buildRenderValues() {
    const objectFields = this.objectInstance.obj_fields;
    const typeFields = this.currentType.fields;

    Object.entries(objectFields).forEach(
      ([key, value]) => {
        const searchField: any = value;
        //console.log(typeFields);
        const test: any = typeFields[searchField.name];
        console.log(searchField);
        //console.log(test.type);
      }
    );
  }

  public revert() {
    console.log('revert');
  }

  public update(instance: any) {
    const newInstance = new CmdbObject();
    console.log('update' + newInstance);
  }

}
