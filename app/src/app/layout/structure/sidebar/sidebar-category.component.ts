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
import { CmdbType } from '../../../framework/models/cmdb-type';
import { ApiCallService } from '../../../services/api-call.service';
import { TypeService } from '../../../framework/services/type.service';

@Component({
  selector: 'cmdb-sidebar-category',
  templateUrl: './sidebar-category.component.html',
  styleUrls: ['./sidebar.component.scss']
})
export class SidebarCategoryComponent implements OnInit {

  @Input() categoryData: any;
  public categoryPopUp: any[];
  public categoryTypeList: CmdbType[];

  constructor(private api: ApiCallService, private typeService: TypeService) {
  }

  ngOnInit() {
    this.initCategoryTypeList();
  }

  private initCategoryTypeList() {
    if (this.categoryData.category.root) {
      this.typeService.getTypeListByCategory(0).subscribe((data: CmdbType[]) => {
        this.categoryTypeList = data;
      });
    } else {
      this.typeService.getTypeListByCategory(this.categoryData.category.public_id).subscribe((data: CmdbType[]) => {
        this.categoryTypeList = data;
      });
    }
  }

  public get_objects_by_type() {
    this.categoryPopUp = [];
    this.initCategoryTypeList();

    for (const type of this.categoryTypeList) {
      const typeID = type.public_id;
      let currentTypeLabel = '';
      let currentTypeIcon = '';
      let amount = '';
      this.api.callGetRoute('type/' + typeID).subscribe((data: CmdbType) => {
        currentTypeLabel = data.label;
        currentTypeIcon = data.render_meta.icon;
        this.api.callGetRoute('object/count/' + typeID).subscribe(ack => {
          amount = ack;
          const popUp = {
            id: typeID,
            label: currentTypeLabel,
            count: amount,
            icon: currentTypeIcon
          };
          this.categoryPopUp.push(popUp);
        });
      });
    }
  }
}
