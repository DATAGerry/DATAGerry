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
import { TypeService } from '../../../framework/services/type.service';
import { ObjectService } from '../../../framework/services/object.service';

@Component({
  selector: 'cmdb-sidebar-category',
  templateUrl: './sidebar-category.component.html',
  styleUrls: ['./sidebar-category.component.scss'],
})
export class SidebarCategoryComponent implements OnInit {

  @Input() categoryData: any;
  public categoryPopUp: any[];

  constructor(private typeService: TypeService) {
  }

  ngOnInit() {
    this.initCategoryTypeList();
  }

  private initCategoryTypeList() {
    if (this.categoryData.category.public_id === 0) {
      this.typeService.getUncategorizedTypes().subscribe((data: CmdbType[]) => {
        this.categoryPopUp = data;
      });
    } else {
      this.typeService.groupTypeByCategory(this.categoryData.category.public_id).subscribe((data: CmdbType[]) => {
        this.categoryPopUp = data;
      });
    }
  }

  public get_objects_by_type() {
    this.initCategoryTypeList();
  }
}
