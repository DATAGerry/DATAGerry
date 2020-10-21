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
import {ObjectService} from '../../framework/services/object.service';
import {TypeService} from '../../framework/services/type.service';
import {SidebarTypeComponent} from '../structure/sidebar/sidebar-type.component';

@Injectable({
  providedIn: 'root'
})
export class SidebarService {

  /**
   * Basic tree observer.
   */
  private categoryTreeObserver = new BehaviorSubject<CmdbCategoryTree>(new CmdbCategoryTree());
  private sideBarType: SidebarTypeComponent[] = [];

  constructor(private categoryService: CategoryService, private objectService: ObjectService, private typeService: TypeService) {

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

  private async updateObjectCount(typeID, tree?: CmdbCategoryTree) {
    let categoryTree = [];
    if (tree && tree.length === 0) {
      categoryTree = tree;
    } else {
      categoryTree = this.categoryTreeObserver.getValue();
    }
    if (categoryTree.length !== 0) {
      return new Promise((resolve) => {
        Array.from(categoryTree).forEach((c: any) => {
          for (const t of c.types) {
            if (typeID === t.public_id) {
              this.objectService.countObjectsByType(typeID).subscribe((data: number) => {
                resolve(data);
              });
            }
          }
        });
      });
    } else {
      return new Promise((resolve) => {
        this.objectService.countObjectsByType(typeID).subscribe((data: number) => {
          resolve(data);
        });
    });
    }
  }

  public async updateTypeCounter(typeID) {
    const sidebarType = this.sideBarType.filter(type => type.type.public_id === typeID).pop()
    console.log(sidebarType);

    const num = await this.updateObjectCount(sidebarType.type.public_id);
    sidebarType.objectCounter = num;
  }

  public async initializeCounter(sidebarType: SidebarTypeComponent) {
    this.sideBarType.push(sidebarType);
    const num = await this.updateObjectCount(sidebarType.type.public_id);
    console.log(num + ":" + sidebarType.type.public_id)
    sidebarType.setCount(num);
  }
}
