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

import { Component, OnInit } from '@angular/core';
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

@Component({
  selector: 'cmdb-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss']
})
export class DashboardComponent implements OnInit {

  public objectCount: number;
  public typeCount: number;
  public userCount: number;
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

  constructor(private api: ApiCallService, private typeService: TypeService,
              private objectService: ObjectService, private categoryService: CategoryService,
              private userService: UserService, private groupService: GroupService) {
  }

  public ngOnInit(): void {
    this.api.callGetRoute('object/count/').subscribe((count) => {
      this.objectCount = count;
    });

    this.api.callGetRoute('type/count/').subscribe((count) => {
      this.typeCount = count;
    });

    this.api.callGetRoute('user/count/').subscribe((count) => {
      this.userCount = count;
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
    let values;
    this.typeService.getTypeList().subscribe((data: CmdbType[]) => {
      values = data;
      }, error => {},
      () => {
        values.forEach(type => {
          this.labelsObject.push(type.label);
          this.colorsObject.push(this.getRandomColor());
          this.objectService.countObjectsByType(type.public_id).subscribe(count => this.itemsObject.push(count));
        });
      });
  }

  private generateTypeChar() {
    this.categoryService.getCategoryList().subscribe((data: CmdbCategory[]) => {
        data.forEach(category => {
          this.labelsCategory.push(category.label);
          this.colorsCategory.push(this.getRandomColor());
          if (category.root) {
            this.typeService.getTypeListByCategory(0).subscribe((list: any[]) => {
              this.itemsCategory.push(list.length);
            });
          } else {
            this.typeService.getTypeListByCategory(category.public_id).subscribe((list: any[]) => {
              this.itemsCategory.push(list.length);
            });
          }
        });
      });
  }

  private generateGroupChar() {
    let values;
    this.groupService.getGroupList().subscribe((data: Group[]) => {
        values = data;
      }, (error) => {},
      () => {
        values.forEach(group => {
          this.labelsGroup.push(group.label);
          this.colorsGroup.push(this.getRandomColor());
          this.userService.getUserByGroup(group.public_id).subscribe((users: User[]) => {
            this.itemsGroup.push(users.length);
          });
        });
      });
  }

  getRandomColor() {
    const color = Math.floor(0x1000000 * Math.random()).toString(16);
    return '#' + ('000000' + color).slice(-6);
  }
}
