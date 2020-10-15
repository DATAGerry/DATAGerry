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
import { UserFormComponent } from '../components/user-form/user-form.component';
import { userExistsValidator, UserService } from '../../services/user.service';
import { GroupService } from '../../services/group.service';
import { ReplaySubject } from 'rxjs';
import { takeUntil } from 'rxjs/operators';
import { Group } from '../../models/group';
import { APIGetMultiResponse, APIInsertSingleResponse } from '../../../services/models/api-response';
import { AuthService } from '../../../auth/services/auth.service';
import { User } from '../../models/user';
import { ToastService } from '../../../layout/toast/toast.service';
import { ActivatedRoute, Router } from '@angular/router';

@Component({
  selector: 'cmdb-user-add',
  templateUrl: './user-add.component.html',
  styleUrls: ['./user-add.component.scss']
})
export class UserAddComponent implements AfterViewInit, OnDestroy {

  /**
   * UserFormComponent for static inserting of parameters.
   */
  @ViewChild(UserFormComponent, { static: true }) userFormComponent: UserFormComponent;

  /**
   * Component un-subscriber.
   */
  private subscriber: ReplaySubject<void> = new ReplaySubject<void>();

  /**
   * List of possible groups.
   */
  public groups: Array<Group> = [];

  /**
   * List of possible auth providers.
   */
  public providers: Array<any> = [];

  constructor(private route: ActivatedRoute, private router: Router,
              private userService: UserService, private toastService: ToastService) {
    this.groups = this.route.snapshot.data.groups as Array<Group>;
    this.providers = this.route.snapshot.data.providers as Array<any>;
  }


  public ngAfterViewInit(): void {
    this.userFormComponent.usernameControl.setAsyncValidators(userExistsValidator(this.userService));
  }

  public ngOnDestroy(): void {
    this.subscriber.next();
    this.subscriber.complete();
  }

  public save(user: User): void {
    this.userService.postUser(user).pipe(takeUntil(this.subscriber)).subscribe((apiUser: User) => {
      this.toastService.success(`User ${apiUser.user_name} was added`);
      this.router.navigate(['/', 'management', 'users']);
    });
  }

}
