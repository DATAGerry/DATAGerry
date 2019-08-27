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

import { Component, OnInit } from '@angular/core';
import { CategoryService } from '../../services/category.service';
import { CmdbCategory } from '../../models/cmdb-category';
import { TypeService } from '../../services/type.service';
import { CmdbType } from '../../models/cmdb-type';

@Component({
  selector: 'cmdb-category-list',
  templateUrl: './category-list.component.html',
  styleUrls: ['./category-list.component.scss']
})
export class CategoryListComponent implements OnInit {

  public categoryList: CmdbCategory[];
  public typeList: CmdbType[];

  constructor(public categoryService: CategoryService, public typeService: TypeService) {

  }

  public ngOnInit(): void {
    this.categoryService.getCategoryList().subscribe((list: CmdbCategory[]) => {
      this.categoryList = list;
    });
  }

}
