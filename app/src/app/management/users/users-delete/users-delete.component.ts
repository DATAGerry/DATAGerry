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
import { ActivatedRoute, Router } from '@angular/router';
import { Observable, Subscription } from 'rxjs';
import { User } from '../../models/user';
import { UserService } from '../../services/user.service';
import { ToastService } from '../../../layout/toast/toast.service';

@Component({
  selector: 'cmdb-users-delete',
  templateUrl: './users-delete.component.html',
  styleUrls: ['./users-delete.component.scss']
})
export class UsersDeleteComponent implements OnInit, OnDestroy {

  // ROUTE PARAMS
  private routeParamObserver: Observable<any>;
  private routeParamSubscription: Subscription;

  // USER DATA
  public userID: number;
  public deleteUser: User;
  private userServiceObserver: Observable<User>;
  private userServiceSubscription: Subscription;

  // Action
  private userDeleteObserver: Observable<boolean>;
  private userDeleteSubscription: Subscription;

  constructor(private userService: UserService, private router: Router, private route: ActivatedRoute,
              private toast: ToastService) {
    this.routeParamObserver = this.route.params;
  }

  public ngOnInit(): void {
    this.routeParamSubscription = this.routeParamObserver.subscribe(
      (params) => {
        this.userID = params.publicID;
        this.userServiceObserver = this.userService.getUser(this.userID);
        this.userServiceSubscription = this.userServiceObserver.subscribe((user: User) => {
          this.deleteUser = user;
        });
      }
    );
  }

  public ngOnDestroy(): void {
    this.routeParamSubscription.unsubscribe();
    this.userServiceSubscription.unsubscribe();
    this.userDeleteSubscription.unsubscribe();
  }

  public onDelete(): void {
    this.userDeleteObserver = this.userService.deleteUser(this.userID);
    this.userDeleteSubscription = this.userDeleteObserver.subscribe((ack: boolean) => {
        this.toast.show('User was deleted');
      },
      (error) => {
        this.toast.error(error.error.description);
      }
    ).add(() => {
      this.router.navigate(['/management/users']);
    });
  }

}
