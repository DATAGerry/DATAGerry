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
import {CmdbType} from "../../../framework/models/cmdb-type";
import {ApiCallService} from "../../../services/api-call.service";

@Component({
  selector: 'cmdb-sidebar-category',
  templateUrl: './sidebar-category.component.html',
  styleUrls: ['./sidebar.component.scss']
})
export class SidebarCategoryComponent implements OnInit {

  @Input() categoryData: any;
  private typeList: CmdbType[] = [];
  private object_count = [];
  constructor(private api: ApiCallService,) { }

  ngOnInit() {

  }

  public get_objects_by_type(category_type_list){
    this.typeList = []

    for(let typ of category_type_list){
      this.api.callGetRoute("type/"+typ).subscribe((list: CmdbType[]) => {
          this.typeList = this.typeList.concat(list);
        },
        () => {

        },
        () => {
          this.count_objects(typ);
        });
    }
  }

  private count_objects(typ){
    this.api.callGetRoute("object/count/"+typ).subscribe((count) => {
        this.object_count.push(count);
      },
      () => {

      },
      () => {
        let c = this.object_count.values();
        for(let typ of this.typeList){
          typ['obj_counter'] = c.next().value;
        }
      });
  }
}
