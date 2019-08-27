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

@Component({
  selector: 'cmdb-sidebar-category',
  templateUrl: './sidebar-category.component.html',
  styleUrls: ['./sidebar.component.scss']
})
export class SidebarCategoryComponent implements OnInit {

  @Input() categoryData: any;
  public categoryPopUp: any[];

  constructor(private api: ApiCallService) {
  }

  ngOnInit() {
  }

  public get_objects_by_type(categoryTypeList) {
    this.categoryPopUp = [];
    for (const typeID of categoryTypeList) {
      let currentTypeLabel = '';
      let amount = '';
      this.api.callGetRoute('type/' + typeID).subscribe((data: CmdbType) => {
        currentTypeLabel = data.label;
        this.api.callGetRoute('object/count/' + typeID).subscribe(ack => {
          amount = ack;
          const popUp = {
            id: typeID,
            label: currentTypeLabel,
            count: amount
          };
          this.categoryPopUp.push(popUp);
        });
      });
    }
  }
}
