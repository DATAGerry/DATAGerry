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

import { AfterViewInit, Component, OnDestroy, OnInit } from '@angular/core';
import { User } from '../models/user';
import { APIGetMultiResponse } from '../../services/models/api-response';
import { UserService } from '../services/user.service';
import { Subject } from 'rxjs';
import { takeUntil } from 'rxjs/operators';

@Component({
  selector: 'cmdb-users',
  templateUrl: './users.component.html',
  styleUrls: ['./users.component.scss']
})
export class UsersComponent implements OnInit, AfterViewInit, OnDestroy {

  private unSubscriber: Subject<void>;
  public dtTrigger: Subject<void> = new Subject();

  public users: Array<User>;
  private apiUsersResponse: APIGetMultiResponse<User>;

  constructor(private userService: UserService) {
    this.unSubscriber = new Subject<void>();
    this.dtTrigger = new Subject<void>();
  }

  public ngOnInit(): void {
    this.userService.getUsers().pipe(takeUntil(this.unSubscriber))
      .subscribe((apiUsersResponse: APIGetMultiResponse<User>) => {
        this.apiUsersResponse = apiUsersResponse;
        this.users = this.apiUsersResponse.results as Array<User>;
      });
  }

  public ngAfterViewInit(): void {
    this.dtTrigger.next();
  }

  public ngOnDestroy(): void {
    this.unSubscriber.next();
    this.unSubscriber.complete();
  }

}
