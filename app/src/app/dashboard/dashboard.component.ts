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

import { Component, OnInit, TemplateRef, ViewChild } from '@angular/core';
import { ApiCallService } from '../services/api-call.service';
import { TypeService } from '../framework/services/type.service';
import { CmdbType } from '../framework/models/cmdb-type';
import { ObjectService } from '../framework/services/object.service';
import { CmdbCategory } from '../framework/models/cmdb-category';
import { CategoryService } from '../framework/services/category.service';
import { GroupService } from '../management/services/group.service';
import { Group } from '../management/models/group';
import { UserService } from '../management/services/user.service';
import { User } from '../management/models/user';
import { APIGetMultiResponse } from '../services/models/api-response';
import { SpecialService } from '../framework/services/special.service';
import { RenderResult } from '../framework/models/cmdb-render';
import { Column } from '../layout/table/table.types';
import { DatePipe } from '@angular/common';

@Component({
  selector: 'cmdb-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss']
})
export class DashboardComponent implements OnInit {

  @ViewChild('activeTemplate', { static: true }) activeTemplate: TemplateRef<any>;
  @ViewChild('userTemplate', { static: true }) userTemplate: TemplateRef<any>;
  @ViewChild('actionTemplate', { static: true }) actionTemplate: TemplateRef<any>;


  public objectCount: number;
  public typeCount: number;
  public userCount: number;

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

  public newestObjects: Array<RenderResult>;
  public newestTableColumns: Array<Column>;
  public newestObjectsCount: number;

  public latestObjects: Array<RenderResult>;
  public latestTableColumns: Array<Column>;
  public latestObjectsCount: number;

  constructor(private api: ApiCallService, private typeService: TypeService,
              private objectService: ObjectService, private categoryService: CategoryService,
              private userService: UserService, private groupService: GroupService,
              private specialService: SpecialService<RenderResult>) {
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

    const creationColumn = {
      display: 'Creation Time',
      name: 'creation_time',
      data: 'object_information.creation_time',
      sortable: false,
      searchable: false,
      cssClasses: ['text-center'],
      render(data: any, item?: any, column?: Column, index?: number) {
        return new Date(data.$date).toUTCString();
      }
    } as Column;

    const lastModColumn = {
      display: 'Modification Time',
      name: 'last_edit_time',
      data: 'object_information.last_edit_time',
      sortable: false,
      searchable: false,
      cssClasses: ['text-center'],
      render(data: any, item?: any, column?: Column, index?: number) {
        if (!data) {
          return 'No modifications so far.';
        }
        return new Date(data.$date).toUTCString();
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
    this.latestTableColumns = [activeColumn, publicColumn, typeColumn, authorColumn, lastModColumn, actionColumn];

    this.objectService.countObjects().subscribe((totals) => {
      this.objectCount = totals;
    });

    this.typeService.countTypes().subscribe(totals => {
      this.typeCount = totals;
    });

    this.userService.countUsers().subscribe((totals: any) => {
      this.userCount = totals;
    });

    this.specialService.getNewestObjects().subscribe((results: Array<RenderResult>) => {
      this.newestObjects = results;
      this.newestObjectsCount = results.length;
    });

    this.specialService.getLatestObjects().subscribe((results: Array<RenderResult>) => {
      this.latestObjects = results;
      this.latestObjectsCount = results.length;
    });

    this.generateObjectChar();
    this.generateTypeChar();
    this.generateGroupChar();
  }

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
    this.objectService.groupObjectsByType('type_id').subscribe(values => {
      for (const obj of values) {
        this.labelsObject.push(obj.label);
        this.colorsObject.push(this.getRandomColor());
        this.itemsObject.push(obj.count);
      }
    });
  }

  private generateTypeChar() {
    this.categoryService.getCategoryList().subscribe((data: CmdbCategory[]) => {
      for (let i = 0; i < data.length; i++) {
        this.labelsCategory.push(data[i].label);
        this.colorsCategory.push(this.getRandomColor());
        this.typeService.getTypeListByCategory(data[i].public_id).subscribe((list: any[]) => {
          this.itemsCategory.push(list.length);
        });
        if (i === this.maxChartValue) {
          break;
        }
      }
    });
  }

  private generateGroupChar() {
    let values;
    this.groupService.getGroups().subscribe((data: APIGetMultiResponse<Group>) => {
        values = data.results;
      }, (error) => {
      },
      () => {
        for (let i = 0; i < values.length; i++) {
          this.userService.getUsersByGroup(values[i].public_id).subscribe((users: User[]) => {
            this.labelsGroup.push(values[i].label);
            this.colorsGroup.push(this.getRandomColor());
            this.itemsGroup.push(users.length);
          });
          if (i === this.maxChartValue) {
            break;
          }
        }

      });
  }

  getRandomColor() {
    const color = Math.floor(0x1000000 * Math.random()).toString(16);
    return '#' + ('000000' + color).slice(-6);
  }
}
