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

import { Component, OnDestroy, OnInit } from '@angular/core';
import { forkJoin, Observable, Subscription } from 'rxjs';
import { CmdbCategory, CmdbCategoryNode, CmdbCategoryTree } from '../models/cmdb-category';
import { CategoryService } from '../services/category.service';
import { CmdbMode } from '../modes.enum';
import { ActivatedRoute } from '@angular/router';
import { SidebarService } from '../../layout/services/sidebar.service';

@Component({
  selector: 'cmdb-category',
  templateUrl: './category.component.html',
  styleUrls: ['./category.component.scss']
})
export class CategoryComponent implements OnInit, OnDestroy {

  /**
   * Root element of the category tree
   */
  public categoryTree: CmdbCategoryTree;
  /**
   * Rest call subscription for root tree
   */
  private categoryTreeSubscription: Subscription;
  /**
   * Category edit mode
   * Default is a basic tree view
   */
  public mode: CmdbMode = CmdbMode.View;
  /**
   * Route data subscription for mode over route data
   */
  private routeSubscription: Subscription;

  constructor(private categoryService: CategoryService, private route: ActivatedRoute, private sidebarService: SidebarService) {

    this.categoryTreeSubscription = new Subscription();
    this.routeSubscription = new Subscription();

    this.routeSubscription = this.route.data.subscribe((data: any) => {
      if (data.mode) {
        this.mode = data.mode;
      }
    });
  }

  public ngOnInit(): void {
    this.categoryTreeSubscription = this.categoryService.getCategoryTree().subscribe((categoryTree: CmdbCategoryTree) => {
      this.categoryTree = categoryTree;
    });
  }

  public ngOnDestroy(): void {
    this.categoryTreeSubscription.unsubscribe();
  }

  /**
   * Rest caller updates every category in tree
   */
  public onSave(): void {
    const observers = this.saveTree(this.categoryTree);
    forkJoin(observers).subscribe(updateResponse => {
      this.sidebarService.reload();
    });
  }

  /**
   * Recursive tree call. Will generate the observers for the calls
   * @param root node root element
   * @param parentNode node of parent
   */
  private saveTree(root: CmdbCategoryTree, parentNode?: CmdbCategoryNode): Observable<any>[] {
    let observers: Observable<any>[] = [];
    // tslint:disable-next-line:forin
    for (let i = 0; i < root.length; i++) {
      const node = root[i];
      node.category.meta.order = i;
      if (parentNode) {
        node.category.parent = parentNode.category.public_id;
      }
      observers.push(this.categoryService.updateCategory(node.category));
      if (node.children.length > 0) {
        observers = observers.concat(this.saveTree(node.children, node));
      }
    }
    return observers;
  }

}
