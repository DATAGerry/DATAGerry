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
import { ActivatedRoute } from '@angular/router';
import { User } from '../models/user';
import { UserService } from '../services/user.service';
import { GroupService } from '../services/group.service';
import { Group } from '../models/group';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { ToastService } from '../../layout/services/toast.service';

@Component({
  selector: 'cmdb-user-view',
  templateUrl: './user-view.component.html',
  styleUrls: ['./user-view.component.scss']
})
export class UserViewComponent implements OnInit {

  public userID: number;
  public userInstance: User;
  public userGroup: Group;
  public profileForm: FormGroup;
  public passwordChangeForm: FormGroup;

  constructor(private route: ActivatedRoute, private userService: UserService,
              private groupService: GroupService, private toastService: ToastService) {
    this.route.params.subscribe((id) => this.userID = id.publicID);
    this.profileForm = new FormGroup({});
    this.passwordChangeForm = new FormGroup({
      password: new FormControl('', Validators.required)
    });
  }

  public ngOnInit(): void {
    this.userService.getUser(this.userID).subscribe((user: User) => {
        this.userInstance = user;
      },
      (error) => {

      },
      () => {
        this.groupService.getGroup(this.userInstance.group_id).subscribe((groupResp: Group) => {
          this.userGroup = groupResp;
        });
      });
  }

  public onPasswordChange(): void {
    const newPassword = this.passwordChangeForm.get('password').value;
    this.userService.changeUserPassword(this.userInstance.public_id, newPassword).subscribe(res => {
      if (res) {
        this.toastService.show('Password changed!');
        this.passwordChangeForm.reset();
      }

    });
  }

}
