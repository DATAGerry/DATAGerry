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
import { Subscription } from 'rxjs';
import { CmdbCategoryTree } from '../models/cmdb-category';
import { CategoryService } from '../services/category.service';
import { CmdbMode } from '../modes.enum';
import { ActivatedRoute } from '@angular/router';

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

  constructor(private categoryService: CategoryService, private route: ActivatedRoute) {

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

}
