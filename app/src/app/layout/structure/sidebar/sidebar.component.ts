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

import { Component, OnDestroy, OnInit, Renderer2 } from '@angular/core';
import { FormControl } from '@angular/forms';
import { CmdbCategoryTree } from '../../../framework/models/cmdb-category';
import { CategoryService } from '../../../framework/services/category.service';
import { Subscription } from 'rxjs';
import { CmdbType } from '../../../framework/models/cmdb-type';
import { TypeService } from '../../../framework/services/type.service';
import { SidebarService } from '../../services/sidebar.service';
import { APIGetMultiResponse } from '../../../services/models/api-response';

@Component({
  selector: 'cmdb-sidebar',
  templateUrl: './sidebar.component.html',
  styleUrls: ['./sidebar.component.scss'],
})
export class SidebarComponent implements OnInit, OnDestroy {
  // Category data
  public categoryTree: CmdbCategoryTree;
  private categoryTreeSubscription: Subscription;
  // Type data
  public typeList: CmdbType[] = [];
  public unCategorizedTypes: CmdbType[] = [];
  private unCategorizedTypesSubscription: Subscription;
  // Filter
  public filterTerm: FormControl = new FormControl('');
  private filterTermSubscription: Subscription;

  constructor(private sidebarService: SidebarService, private categoryService: CategoryService,
              private typeService: TypeService, private renderer: Renderer2) {
    this.categoryTreeSubscription = new Subscription();
    this.unCategorizedTypesSubscription = new Subscription();
    this.filterTermSubscription = new Subscription();
  }

  public ngOnInit(): void {
    this.renderer.addClass(document.body, 'sidebar-fixed');
    this.categoryTreeSubscription = this.sidebarService.categoryTree.asObservable().subscribe((categoryTree: CmdbCategoryTree) => {
      this.categoryTree = categoryTree;
      this.typeService.countUncategorizedTypes().subscribe((numberUncategorizedTypes: number) => {
        this.unCategorizedTypesSubscription = this.typeService.getUncategorizedTypes({limit: numberUncategorizedTypes}).subscribe(
          (apiResponse: APIGetMultiResponse<CmdbType>) => {
          this.unCategorizedTypes = apiResponse.results as Array<CmdbType>;
        });
      });

      this.typeService.getTypeList().subscribe((types: CmdbType[]) => this.typeList = types);
    });
  }

  public ngOnDestroy(): void {
    this.categoryTreeSubscription.unsubscribe();
    this.unCategorizedTypesSubscription.unsubscribe();
    this.filterTermSubscription.unsubscribe();
    this.renderer.removeClass(document.body, 'sidebar-fixed');
  }

}
