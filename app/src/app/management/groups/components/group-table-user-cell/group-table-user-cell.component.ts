/*
* DATAGERRY - OpenSource Enterprise CMDB
* Copyright (C) 2019 - 2020 NETHINKS GmbH
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

import { Component, Input, OnDestroy } from '@angular/core';
import { Group } from '../../../models/group';
import { UserService } from '../../../services/user.service';
import { ReplaySubject } from 'rxjs';
import { takeUntil } from 'rxjs/operators';

@Component({
  selector: 'cmdb-group-table-user-cell',
  templateUrl: './group-table-user-cell.component.html',
  styleUrls: ['./group-table-user-cell.component.scss']
})
export class GroupTableUserCellComponent implements OnDestroy {

  private subscriber: ReplaySubject<void> = new ReplaySubject<void>();
  public group: Group;
  public numberOfUsers: number;

  @Input('group')
  public set Group(group: Group) {
    this.group = group;
    this.userService.countUsers({group_id: this.group.public_id}).pipe(takeUntil(this.subscriber))
      .subscribe((nUsers: number) => {
        this.numberOfUsers = nUsers;
    });
  }

  constructor(private userService: UserService) {
  }

  public ngOnDestroy(): void {
    this.subscriber.next();
    this.subscriber.complete();
  }

}
