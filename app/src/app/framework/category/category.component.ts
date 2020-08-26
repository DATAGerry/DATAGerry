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

import { AfterViewInit, Component, OnDestroy, OnInit, ViewChild } from '@angular/core';
import { BehaviorSubject, forkJoin, Observable, ReplaySubject, Subject } from 'rxjs';
import { CmdbCategory, CmdbCategoryNode, CmdbCategoryTree } from '../models/cmdb-category';
import { CategoryService } from '../services/category.service';
import { CmdbMode } from '../modes.enum';
import { ActivatedRoute } from '@angular/router';
import { SidebarService } from '../../layout/services/sidebar.service';
import { takeUntil } from 'rxjs/operators';
import { APIGetMultiResponse } from '../../services/models/api-response';
import { CollectionParameters } from '../../services/models/api-parameter';
import { DataTableDirective } from 'angular-datatables';

@Component({
  selector: 'cmdb-category',
  templateUrl: './category.component.html',
  styleUrls: ['./category.component.scss']
})
export class CategoryComponent implements OnInit, AfterViewInit, OnDestroy {

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
   * Datatable datas
   */
  public dtOptions: DataTables.Settings = {};
  public dtTrigger: Subject<void> = new Subject();
  @ViewChild(DataTableDirective, { static: false }) dtElement: DataTableDirective;

  constructor(private categoryService: CategoryService, private route: ActivatedRoute, private sidebarService: SidebarService) {
    this.categories = [];
    this.displayMode = this.displayModeSubject.asObservable();
    this.displayModeSubject.next(this.route.snapshot.data.mode);
  }

  public ngOnInit(): void {
    this.displayMode.pipe(takeUntil(this.unSubscribe)).subscribe((mode: number) => {
      this.categoryService.getCategoryTree().pipe(
        takeUntil(this.unSubscribe)).subscribe((categoryTree: CmdbCategoryTree) => {
        this.categoryTree = categoryTree;
      });
    });
    this.dtOptions = {
      columns: [
        {
          title: 'PublicID',
          name: 'public_id',
          data: 'public_id'
        },
        {
          title: 'Name',
          name: 'name',
          data: 'name'
        },
        {
          title: 'Label',
          name: 'label',
          data: 'label'
        },
        {
          title: 'ParentID',
          name: 'parent',
          data: 'parent'
        }
      ],
      searching: false,
      serverSide: true,
      processing: true,
      ajax: (params: any, callback) => {

        const apiParameters: CollectionParameters = {
          page: Math.ceil(params.start / params.length) + 1,
          limit: params.length,
          sort: params.columns[params.order[0].column].name,
          order: params.order[0].dir === 'desc' ? -1 : 1,
        };

        this.categoryService.getCategoryIteration(apiParameters).pipe(
          takeUntil(this.unSubscribe)).subscribe((response: APIGetMultiResponse<CmdbCategory>) => {
          this.categoriesAPIResponse = response;
          this.categories = this.categoriesAPIResponse.results;
          callback({
            recordsTotal: response.total,
            recordsFiltered: response.total,
            data: this.categories
          });
        });
      }
    };
  }

  public ngAfterViewInit(): void {
    this.dtTrigger.next();
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

  public onTreeChange(event: any): void {
    this.sidebarService.reload();
    this.ngOnInit();
    this.rerender();
  }

  public rerender(): void {
    this.dtElement.dtInstance.then((dtInstance: DataTables.Api) => {
      dtInstance.destroy();
      this.dtTrigger.next();
    });
  }

}
