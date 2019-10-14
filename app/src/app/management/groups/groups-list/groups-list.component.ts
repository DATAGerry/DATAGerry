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

import { Component, OnDestroy, OnInit } from '@angular/core';
import { GroupService } from '../../services/group.service';
import { Group } from '../../models/group';
import { Subject } from 'rxjs';
import { Right } from '../../models/right';
import { RightService } from '../../services/right.service';

@Component({
  selector: 'cmdb-groups-list',
  templateUrl: './groups-list.component.html',
  styleUrls: ['./groups-list.component.scss']
})
export class GroupsListComponent implements OnInit, OnDestroy {

  public groupList: Group[];
  public rightList: Right[];

  public dtOptions: DataTables.Settings = {};
  public dtTrigger: Subject<any> = new Subject();

  constructor(private groupService: GroupService, private rightService: RightService) {
  }

  public ngOnInit(): void {
    this.dtOptions = {
      language: {
        search: '',
        searchPlaceholder: 'Filter...'
      }
    };

    this.groupService.getGroupList().subscribe((groupList: Group[]) => {
        this.groupList = groupList;
      },
      (error) => {
        console.error(error);
      }, () => {
        this.dtTrigger.next();
      }
    );

    this.rightService.getRightList().subscribe((rightList: Right[]) => {
      this.rightList = rightList;
    });
  }

  public ngOnDestroy(): void {
    this.dtTrigger.unsubscribe();
  }

}
