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

import { Component, Input, OnInit } from '@angular/core';
import { CmdbType } from '../../../framework/models/cmdb-type';
import { ApiCallService } from '../../../services/api-call.service';

@Component({
  selector: 'cmdb-sidebar-category',
  templateUrl: './sidebar-category.component.html',
  styleUrls: ['./sidebar.component.scss']
})
export class SidebarCategoryComponent implements OnInit {

  @Input() categoryData: any;

  public typeList: any[] = [];
  private objectCount = [];

  constructor(private api: ApiCallService) {
  }

  ngOnInit() {
  }

  public get_objects_by_type(categoryTypeList) {
    this.typeList = [];

    for (const typ of categoryTypeList) {
      this.api.callGetRoute('type/' + typ).subscribe((list: CmdbType[]) => {
        this.typeList = this.typeList.concat(list);
      }, error => {
      }, () => {
        this.count_objects(typ);
      });
    }
  }

  private count_objects(typ) {
    this.api.callGetRoute('object/count/' + typ).subscribe((count) => {
      this.objectCount.push(count);
    }, error => {
    }, () => {
      const c = this.objectCount.values();
      for (const typ2 of this.typeList) {
        typ2.countObjects = c.next().value;
      }
    });
  }
}
