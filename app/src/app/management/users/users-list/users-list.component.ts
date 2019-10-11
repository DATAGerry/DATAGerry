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

import { Component, OnInit, ViewChild } from '@angular/core';
import { GroupService } from '../../services/group.service';
import { UserService } from '../../services/user.service';
import { DataTableDirective } from 'angular-datatables';
import { Subject } from 'rxjs';
import { User } from '../../models/user';
import { Group } from '../../models/group';

@Component({
  selector: 'cmdb-users-list',
  templateUrl: './users-list.component.html',
  styleUrls: ['./users-list.component.scss']
})
export class UsersListComponent implements OnInit {

  public userList: User[];
  public groupList: Group[];

  @ViewChild(DataTableDirective, { static: false })
  private dtElement: DataTableDirective;

  public dtOptions: any = {};
  public dtTrigger: Subject<any> = new Subject();

  constructor(private userService: UserService, public groupService: GroupService) {
  }

  public ngOnInit(): void {
    this.dtOptions = {
      ordering: true,
      order: [[0, 'asc']],
      rowGroup: {
        endRender(rows, group) {
          return `Number of users in this group: ${ rows.count() }`;
        },
        dataSrc: 5
      },
      language: {
        search: '',
        searchPlaceholder: 'Filter...'
      }
    };
    this.groupService.getGroupList().subscribe((groups: Group[]) => {
      this.groupList = groups;
      this.userService.getUserList().subscribe((users: User[]) => {
          this.userList = users;

        },
        (error) => {
          console.error(error);
        }, () => {
          this.dtTrigger.next();
        }
      );
    });
  }

  public findGroup(publicID) {
    return this.groupList.find(g => g.public_id === publicID);
  }

}
