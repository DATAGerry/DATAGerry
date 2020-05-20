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
import { TypeService } from '../../../framework/services/type.service';
import { CmdbCategoryNode } from '../../../framework/models/cmdb-category';

@Component({
  selector: 'cmdb-sidebar-category',
  templateUrl: './sidebar-category.component.html',
  styleUrls: ['./sidebar-category.component.scss'],
})
export class SidebarCategoryComponent implements OnInit {

  @Input() categoryNode: CmdbCategoryNode;

  constructor(private typeService: TypeService) {
  }

  ngOnInit() {
    console.log(this.categoryNode);
  }

}
