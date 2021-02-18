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

import { Component, Input, OnInit } from '@angular/core';
import { TypeService } from '../../../../services/type.service';
import { ConfigEditBaseComponent } from '../config.edit';
import { RenderResult } from '../../../../models/cmdb-render';
import { ObjectService } from '../../../../services/object.service';
import { CmdbType } from '../../../../models/cmdb-type';

@Component({
  selector: 'cmdb-ref-field-edit',
  templateUrl: './ref-field-edit.component.html',
  styleUrls: ['./ref-field-edit.component.scss']
})
export class RefFieldEditComponent extends ConfigEditBaseComponent implements OnInit {
  @Input() groupList: any;
  @Input() userList: any;
  public typeList: CmdbType[];
  public objectList: RenderResult[] = [];

  constructor(private typeService: TypeService, private objectService: ObjectService) {
    super();
  }

  public ngOnInit(): void {
    this.typeService.getTypeList().subscribe((res: CmdbType[]) => {
      this.typeList = res;
    });

    if (this.data.value !== null && this.data.value !== undefined && this.data.value !== '') {
      this.objectService.getObjectsByType(this.data.ref_types).subscribe((res: RenderResult[]) => {
        this.objectList = res;
      });
    }

    if (this.data.ref_types) {
      if (!Array.isArray(this.data.ref_types)) {
        this.data.ref_types = [this.data.ref_types];
      }
    }
  }

  public onChange() {
    const {ref_types} = this.data;
    if (ref_types && ref_types.length === 0) {
      this.objectList = [];
      this.data.value = '';
    } else {
      this.objectService.getObjectsByType(ref_types).subscribe((res: RenderResult[]) => {
        this.objectList = res;
      });
    }
  }

  public changeDefault(value: any) {
    this.data.default = parseInt(value, 10);
    return this.data.default;
  }
}
