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
* along with this program. If not, see <https://www.gnu.org/licenses/>.
*/

import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';
import { CmdbCategoryTree } from '../../framework/models/cmdb-category';
import { CategoryService } from '../../framework/services/category.service';

@Injectable({
  providedIn: 'root'
})
export class SidebarService {

  /**
   * Basic tree observer.
   */
  private categoryTreeObserver = new BehaviorSubject<CmdbCategoryTree>(new CmdbCategoryTree());

  constructor(private categoryService: CategoryService) {
    this.categoryService.getCategoryTree().subscribe((tree: CmdbCategoryTree)  => {
      this.categoryTreeObserver.next(tree);
    });
  }

  /**
   * Get the subject of the current category tree.
   */
  public get categoryTree(): BehaviorSubject<CmdbCategoryTree> {
    return this.categoryTreeObserver;
  }

  /**
   * Reload the category tree.
   */
  public reload() {
    this.categoryService.getCategoryTree().subscribe((tree: CmdbCategoryTree)  => {
      this.categoryTreeObserver.next(tree);
    });
  }
}
