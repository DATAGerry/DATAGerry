/*
* DATAGERRY - OpenSource Enterprise CMDB
* Copyright (C) 2023 becon GmbH
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
*
* You should have received a copy of the GNU Affero General Public License
* along with this program. If not, see <https://www.gnu.org/licenses/>.
*/


import { Component, OnDestroy, OnInit, TemplateRef, ViewChild } from '@angular/core';

import { takeUntil } from 'rxjs/operators';
import { ReplaySubject } from 'rxjs';

import { TypeService } from '../framework/services/type.service';
import { ObjectService } from '../framework/services/object.service';
import { CategoryService } from '../framework/services/category.service';
import { GroupService } from '../management/services/group.service';
import { UserService } from '../management/services/user.service';
import { ToastService } from '../layout/toast/toast.service';
import { SidebarService } from '../layout/services/sidebar.service';

import { CmdbCategory } from '../framework/models/cmdb-category';
import { Group } from '../management/models/group';
import { APIGetMultiResponse } from '../services/models/api-response';
import { RenderResult } from '../framework/models/cmdb-render';
import { Column } from '../layout/table/table.types';
import { CollectionParameters } from '../services/models/api-parameter';
import { CmdbType } from '../framework/models/cmdb-type';
/* -------------------------------------------------------------------------- */

@Component({
  selector: 'cmdb-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss']
})
export class DashboardComponent implements OnInit, OnDestroy {

  /**
   * Table Template: Dashboard active column.
   */
  @ViewChild('activeTemplate', { static: true }) activeTemplate: TemplateRef<any>;

  /**
   * Table Template: Dashboard user column.
   */
  @ViewChild('userTemplate', { static: true }) userTemplate: TemplateRef<any>;

  /**
   * Table Template: Dashboard action column.
   */
  @ViewChild('actionTemplate', { static: true }) actionTemplate: TemplateRef<any>;

  /**
   * Table Template: Dashboard date column.
   */
  @ViewChild('dateTemplate', { static: true }) dateTemplate: TemplateRef<any>;

  /**
   * Global unsubscriber for http calls to the rest backend.
   */
  private unSubscribe: ReplaySubject<void> = new ReplaySubject();

  public objectCount: number = 0;
  public typeCount: number = 0;
  public userCount: number = 0;

  public readonly maxChartValue: number = 4;

  // Chart Objects
  public labelsObject: string [] = [];
  public itemsObject: number [] = [];
  public colorsObject: any [] = [];
  public optionsObject: {} = {};

  // Chart Types
  public labelsCategory: string [] = [];
  public itemsCategory: number [] = [];
  public colorsCategory: any [] = [];

  // Chart Users
  public labelsGroup: string [] = [];
  public itemsGroup: number [] = [];
  public colorsGroup: any [] = [];

  public newestObjects: Array<RenderResult> = [];
  public newestTableColumns: Array<Column> = [];
  public newestObjectsCount: number = 0;
  public readonly newestInnitPage: number = 1;
  public newestPage: number = this.newestInnitPage;
  public newestLoading: boolean = false;

  public latestObjects: Array<RenderResult> = [];
  public latestTableColumns: Array<Column> = [];
  public latestObjectsCount: number = 0;
  public readonly latestInnitPage: number = 1;
  public latestPage: number = this.latestInnitPage;
  public latestLoading: boolean = false;

/* -------------------------------------------------------------------------- */
/*                                 LIFE CYCLE                                 */
/* -------------------------------------------------------------------------- */

  constructor(private typeService: TypeService,
              private objectService: ObjectService, 
              private categoryService: CategoryService,
              private toastService: ToastService, 
              private sidebarService: SidebarService,
              private userService: UserService, 
              private groupService: GroupService) {
  }

  public ngOnInit(): void {

    const activeColumn = {
      display: 'Active',
      name: 'active',
      data: 'object_information.active',
      searchable: false,
      sortable: false,
      template: this.activeTemplate,
      cssClasses: ['text-center'],
      style: { width: '6rem' }
    } as unknown as Column;

    const publicColumn = {
      display: 'Public ID',
      name: 'public_id',
      data: 'object_information.object_id',
      cssClasses: ['text-center'],
      style: { width: '6rem' },
      searchable: false,
      sortable: false
    } as unknown as Column;

    const typeColumn = {
      display: 'Type',
      name: 'type',
      data: 'type_information.type_label',
      cssClasses: ['text-center'],
      searchable: false,
      sortable: false
    } as unknown as Column;

    const authorColumn = {
      display: 'Author',
      name: 'author_id',
      data: 'object_information.author_name',
      sortable: false,
      searchable: false,
      cssClasses: ['text-center']
    } as Column;

    const editorColumn = {
      display: 'Last editor',
      name: 'editor_id',
      data: 'object_information.editor_name',
      sortable: false,
      searchable: false,
      cssClasses: ['text-center'],
      render(data: any) {
        if (!data) {
          return '';
        }
        return data;
      }
    } as Column;

    const creationColumn = {
      display: 'Creation Time',
      name: 'creation_time',
      data: 'object_information.creation_time',
      sortable: false,
      searchable: false,
      cssClasses: ['text-center'],
      template: this.dateTemplate,
    } as Column;

    const lastModColumn = {
      display: 'Modification Time',
      name: 'last_edit_time',
      data: 'object_information.last_edit_time',
      sortable: false,
      searchable: false,
      cssClasses: ['text-center'],
      template: this.dateTemplate,
      render(data: any) {
        if (!data) {
          return 'No modifications so far.';
        }
        return data;
      }
    } as Column;

    const actionColumn = {
      display: 'Actions',
      name: 'actions',
      sortable: false,
      searchable: false,
      fixed: true,
      template: this.actionTemplate,
      cssClasses: ['text-center'],
      style: { width: '6em' }
    } as unknown as Column;
    this.newestTableColumns = [activeColumn, publicColumn, typeColumn, authorColumn, creationColumn, actionColumn];
    this.latestTableColumns = [activeColumn, publicColumn, typeColumn, editorColumn, lastModColumn, actionColumn];

    this.countTypes();
    this.countObjects();

    this.userService.countUsers().pipe(takeUntil(this.unSubscribe)).subscribe((totals: any) => {
      this.userCount = totals;
    });

    this.loadNewestObjects();
    this.loadLatestObjects();

    this.generateObjectChar();
    this.generateTypeChar();
    this.generateGroupChar();
  }

  public ngOnDestroy(): void {
    this.unSubscribe.next();
    this.unSubscribe.complete();
  }

/* -------------------------------------------------------------------------- */
/*                                 OBJECTS API                                */
/* -------------------------------------------------------------------------- */


  /**
   * Returns the number of objects
   */
  private countObjects(): void {
    const apiParameters: CollectionParameters = { limit: 1, sort: 'public_id', order: 1, page: 1,
      filter: [{ $match: { } }]};
    this.objectService.getObjects(apiParameters).pipe(takeUntil(this.unSubscribe))
      .subscribe((apiResponse: APIGetMultiResponse<RenderResult>) => {
        this.objectCount = apiResponse.total;
      });
  }

  /**
   * Gets newest objects
   */
  private loadNewestObjects(): void {
    this.newestLoading = true;
    const apiParameters: CollectionParameters = {page: this.newestPage, limit: 10, order: -1};
    this.objectService.getNewestObjects(apiParameters).pipe(takeUntil(this.unSubscribe))
      .subscribe((apiResponse: APIGetMultiResponse<RenderResult>) => {
      this.newestObjects = apiResponse.results as Array<RenderResult>;
      this.newestObjectsCount = apiResponse.total;
    }, () => {}, () => {
        this.newestLoading = false;
      } );
  }


  private loadLatestObjects(): void {
    this.latestLoading = true;
    const apiParameters: CollectionParameters = {page: this.latestPage, limit: 10, order: -1};
    this.objectService.getLatestObjects(apiParameters).pipe(takeUntil(this.unSubscribe))
      .subscribe((apiResponse: APIGetMultiResponse<RenderResult>) => {
      this.latestObjects = apiResponse.results as Array<RenderResult>;
      this.latestObjectsCount = apiResponse.total;
    }, () => {}, () => {
        this.latestLoading = false;
      } );
  }


  public onObjectDelete(value: RenderResult) {
    this.objectService.deleteObject(value.object_information.object_id, true).pipe(takeUntil(this.unSubscribe))
      .subscribe(() => {
          this.toastService.success(`Object ${ value.object_information.object_id } was deleted successfully`);
          this.sidebarService.updateTypeCounter(value.type_information.type_id).then(() => {
              this.loadLatestObjects();
              this.loadNewestObjects();
            }
          );
        },
        (error) => {
          this.toastService.error(`Error while deleting object ${ value.object_information.object_id } | Error: ${ error }`);
        }
        );
  }

  public onObjectDeleteWithLocations(value: RenderResult){
    console.log("delete with locations");
  }

  public onObjectDeleteWithObjects(value: RenderResult){
    console.log("delete with objects");
  }

/* -------------------------- OBJECTS API - HELPER -------------------------- */

public onNewestPageChange(event) {
  this.newestPage = event;
  this.loadNewestObjects();
}

public  onLatestPageChange(event) {
  this.latestPage = event;
  this.loadLatestObjects();
}

/* -------------------------------------------------------------------------- */
/*                                  TYPES API                                 */
/* -------------------------------------------------------------------------- */

  /**
   * Returns the number number of types
   */
  private countTypes(): void {
    const filter = JSON.stringify(this.typeService.getAclFilter());
    const apiParameters: CollectionParameters = { page: 1, limit: 1, sort: 'public_id', order: 1, filter};
    this.typeService.getTypes(apiParameters).pipe(takeUntil(this.unSubscribe))
      .subscribe((response: APIGetMultiResponse<CmdbType>) => {
        this.typeCount = response.total;
      });
  }


/* -------------------------------------------------------------------------- */
/*                              CHARTS FUNCTIONS                              */
/* -------------------------------------------------------------------------- */

  private generateObjectChar() {
    this.optionsObject = {
      responsive: true,
      legend: {
        display: false
      },
      scales: {
        yAxes: [{
          ticks: {
            beginAtZero: true
          }
        }]
      },
    };
    this.objectService.groupObjectsByType('type_id').pipe(takeUntil(this.unSubscribe)).subscribe(values => {
      for (const obj of values) {
        this.labelsObject.push(obj.label);
        this.colorsObject.push(this.getRandomColor());
        this.itemsObject.push(obj.count);
      }
    });
  }

  private generateTypeChar() {
    const params = {
      filter: undefined,
      limit: 5,
      sort: 'public_id',
      order: 1,
      page: 1,
      view: 'tree'
    };
    this.categoryService.getCategories(params).pipe(takeUntil(this.unSubscribe))
      .subscribe((apiResponse: APIGetMultiResponse<CmdbCategory>) => {
        const categories = apiResponse.results as Array<CmdbCategory>;
        for (const cate of categories) {
          this.labelsCategory.push(cate.label);
          this.colorsCategory.push(this.getRandomColor());

          if (cate.types.length !== 0) {
            this.itemsCategory.push(cate.types.length);
          } else {
            this.itemsCategory.push(null);
          }
        }
      });
  }

  private generateGroupChar() {
    const groupsCallParameters: CollectionParameters = {
      filter: [{
        $lookup:
          {
            from: 'management.users',
            localField: 'public_id',
            foreignField: 'group_id',
            as: 'users'
          }
      }],
      limit: 5,
      sort: 'public_id',
      order: 1,
      page: 1
    };

    this.groupService.getGroups(groupsCallParameters).subscribe((data: APIGetMultiResponse<Group>) => {
        for (let i = 0; i < data.results.length; i++) {
          this.userService.countUsers({group_id: data.results[i].public_id}).pipe(takeUntil(this.unSubscribe))
            .subscribe((nUsers: number) => {
              this.labelsGroup.push(data.results[i].label);
              this.colorsGroup.push(this.getRandomColor());
              this.itemsGroup.push(nUsers);
            });
          if (i === this.maxChartValue) {
            break;
          }
        }
      });
  }

  /* ------------------------------ CHARTS HELPER ----------------------------- */
  getRandomColor() {
    const color = Math.floor(0x1000000 * Math.random()).toString(16);
    return '#' + ('000000' + color).slice(-6);
  }
}
