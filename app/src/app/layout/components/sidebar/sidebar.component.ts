/*
* dataGerry - OpenSource Enterprise CMDB
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
import { ApiCallService } from '../../../services/api-call.service';
import { FormControl } from '@angular/forms';
import { CmdbType } from '../../../framework/models/cmdb-type';

@Component({
  selector: 'cmdb-sidebar',
  templateUrl: './sidebar.component.html',
  styleUrls: ['./sidebar.component.scss'],
})
export class SidebarComponent implements OnInit, OnDestroy {
  public categoryTree: any;
  private defaultCategoryTree: any[];
  private filterCategoryTree: any[];
  public filterTerm: FormControl = new FormControl('');

  constructor(private api: ApiCallService, private renderer: Renderer2) {
  }

  public ngOnInit(): void {
    this.renderer.addClass(document.body, 'sidebar-fixed');
    const categoryTreeObserver = this.api.callGetRoute('category/tree');
    categoryTreeObserver.subscribe(tree => {
      this.categoryTree = tree;
      this.defaultCategoryTree = tree;
    });

    this.filterTerm.statusChanges.subscribe(() => {
      this.filterCategoryTree = [];
      this.categoryTree = this.transform(this.categoryTree, this.filterTerm.value);
    });
  }

  public ngOnDestroy(): void {
    this.renderer.removeClass(document.body, 'sidebar-fixed');
  }

  private transform(filterList: any[], searchText: string): any[] {
    if (!filterList) {
      return [];
    }
    if (!searchText) {
      return this.defaultCategoryTree;
    }

    searchText = searchText.toLowerCase();

    for (const it of filterList) {
      let isAvailable = it.category.label.toLowerCase().includes(searchText);
      if (isAvailable) {
        if (this.filterCategoryTree.includes(it) === false) {
          this.filterCategoryTree.push(it);
        }
      } else {
        for (const typ of it.category.type_list) {
          this.api.callGetRoute('type/' + typ).subscribe((obj: CmdbType) => {
            isAvailable = obj.label.toLowerCase().includes(searchText);
            if (isAvailable) {
              if (this.filterCategoryTree.includes(it) === false) {
                this.filterCategoryTree.push(it);
              }
            }
          });
        }
      }
      this.transform(it.children, searchText);
    }
    return this.filterCategoryTree;
  }
}
