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
import { BehaviorSubject, forkJoin, Observable, ReplaySubject } from 'rxjs';
import { CmdbCategory, CmdbCategoryNode, CmdbCategoryTree } from '../models/cmdb-category';
import { CategoryService } from '../services/category.service';
import { CmdbMode } from '../modes.enum';
import { ActivatedRoute } from '@angular/router';
import { SidebarService } from '../../layout/services/sidebar.service';
import { takeUntil } from 'rxjs/operators';
import { APIGetMultiResponse } from '../../services/models/api-response';
import { CollectionParameters } from '../../services/models/api-parameter';
import { Column} from '../../layout/table/table.types';

@Component({
  selector: 'cmdb-category',
  templateUrl: './category.component.html',
  styleUrls: ['./category.component.scss']
})
export class CategoryComponent implements OnInit, OnDestroy {

  /**
   * Global unsubscriber for http calls to the rest backend.
   */
  private unSubscribe: ReplaySubject<void> = new ReplaySubject();

  /**
   * Current category collection
   */
  public categories: Array<CmdbCategory>;
  public categoriesAPIResponse: APIGetMultiResponse<CmdbCategory>;

  /**
   * Root element of the category tree
   */
  public categoryTree: CmdbCategoryTree;

  /**
   * Current display mode
   */
  private displayMode: Observable<CmdbMode>;

  /**
   * Current display mode subject
   */
  private displayModeSubject: BehaviorSubject<CmdbMode> = new BehaviorSubject<CmdbMode>(CmdbMode.View);

  /**
   * Table datas
   */
  public apiParameters: CollectionParameters = {
    limit: 10, sort: 'public_id', order: -1, page: 1
  };
  public tableColumns: Array<Column>;
  public totalResults: number = 0;

  constructor(private categoryService: CategoryService, private route: ActivatedRoute, private sidebarService: SidebarService) {
    this.categories = [];
    this.displayMode = this.displayModeSubject.asObservable();
    this.displayModeSubject.next(this.route.snapshot.data.mode);
  }

  private tableColumnBuilder(): void {

    const publicColumn = {
      display: 'Public ID',
      name: 'public_id',
      data: 'public_id',
      cssClasses: ['text-center'],
      style: { width: '6rem' },
      searchable: false,
      sortable: false
    } as unknown as Column;

    const nameColumn = {
      display: 'Name',
      name: 'name',
      data: 'name',
      cssClasses: ['text-center'],
      searchable: false,
      sortable: false
    } as unknown as Column;

    const labelColumn = {
      display: 'Label',
      name: 'label',
      data: 'label',
      cssClasses: ['text-center'],
      searchable: false,
      sortable: false
    } as unknown as Column;

    const parentColumn = {
      display: 'Parent ID',
      name: 'parent',
      data: 'parent',
      cssClasses: ['text-center'],
      style: { width: '6rem' },
      searchable: false,
      sortable: false
    } as unknown as Column;

    this.tableColumns = [publicColumn, labelColumn, nameColumn, parentColumn];
  }

  /**
   * Load categories from the backend.
   */
  private loadCategories(): void {
    this.categoryService.getCategoryIteration(this.apiParameters).pipe(
      takeUntil(this.unSubscribe)).subscribe((response: APIGetMultiResponse<CmdbCategory>) => {
      this.categoriesAPIResponse = response;
      this.categories = this.categoriesAPIResponse.results;
      this.totalResults = response.total;
    });
  }

  /**
   * Load category tree from the backend.
   */
  private loadCategoryTree(): void {
    this.displayMode.subscribe(() => {
      this.sidebarService.categoryTree.asObservable().pipe(takeUntil(this.unSubscribe))
        .subscribe((categoryTree: CmdbCategoryTree) => {
          this.categoryTree = categoryTree;
      });
    });
  }

  /**
   * Will generate all needed data for cmdb-table.
   */
  private dataLoader(): void {
    this.tableColumnBuilder();
    this.loadCategoryTree();
    this.loadCategories();
  }

  public ngOnInit(): void {
    this.dataLoader();
  }

  /**
   * On table page change.
   * Reload all objects.
   *
   * @param page
   */
  public onPageChange(page: number) {
    this.apiParameters.page = page;
    this.loadCategories();
  }

  /**
   * On table page size change.
   * Reload all objects.
   *
   * @param limit
   */
  public onPageSizeChange(limit: number): void {
    this.apiParameters.limit = limit;
    this.loadCategories();
  }

  public ngOnDestroy(): void {
    this.unSubscribe.next();
    this.unSubscribe.complete();
  }

  public get mode(): CmdbMode {
    return this.displayModeSubject.getValue();
  }

  /**
   * Rest caller updates every category in tree
   */
  public onSave(): void {
    const observers = this.saveTree(this.categoryTree);
    forkJoin(observers).subscribe(() => {
      this.sidebarService.loadCategoryTree();
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
      node.category.meta.order = i + 1;
      if (parentNode) {
        node.category.parent = parentNode.category.public_id;
      }
      if (!parentNode && node.category.parent !== null) {
        node.category.parent = null;
      }
      observers.push(this.categoryService.updateCategory(node.category));
      if (node.children.length > 0) {
        observers = observers.concat(this.saveTree(node.children, node));
      }
    }
    return observers;
  }

  public onTreeChange(): void {
    this.sidebarService.loadCategoryTree();
    this.dataLoader();
  }
}
