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

import { Component, Input, OnInit } from '@angular/core';
import { UserService } from '../../../../../user/services/user.service';
import { User } from '../../../../../user/models/user';
import { Group } from '../../../../../user/models/group';
import { FormControl, FormGroup } from '@angular/forms';
import { GroupService } from '../../../../../user/services/group.service';

@Component({
  selector: 'cmdb-type-access-step',
  templateUrl: './type-access-step.component.html',
  styleUrls: ['./type-access-step.component.scss']
})
export class TypeAccessStepComponent implements OnInit {

  public accessForm: FormGroup;
  public userList: User[] = [];
  public groupList: Group[] = [];

  @Input()
  set preData(data: any) {
    if (data !== undefined) {
      if (data.access !== undefined) {
        this.groups.patchValue(data.access.groups);
        this.users.patchValue(data.access.users);
      }

    }
  }

  constructor(private userService: UserService, private groupService: GroupService) {
    this.accessForm = new FormGroup({
      groups: new FormControl(''),
      users: new FormControl('')
    });
  }

  public get groups() {
    return this.accessForm.get('groups');
  }

  public get users() {
    return this.accessForm.get('users');
  }

  public ngOnInit(): void {

    this.groupService.getGroupList().subscribe((gList: Group[]) => {
      this.groupList = gList;
    });
    this.userService.getUserList().subscribe((uList: User[]) => {
      this.userList = uList;
    });
  }

}
