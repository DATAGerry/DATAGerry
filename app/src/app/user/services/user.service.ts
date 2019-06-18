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

import { Injectable } from '@angular/core';
import { ApiCallService } from '../../services/api-call.service';
import { User } from '../models/user';
import { Group } from '../models/group';
import { AuthService } from '../../auth/services/auth.service';
import { BehaviorSubject, Observable } from 'rxjs';
import { UserToken } from '../../auth/models/user-token';

@Injectable({
  providedIn: 'root'
})
export class UserService {

  private readonly prefix: string = 'user';
  private userList: User[] = [];
  private groupList: Group[] = [];

  private readonly currentUserToken: UserToken;

  constructor(private api: ApiCallService, private authService: AuthService) {
    this.currentUserToken = this.authService.currentUserValue;

    this.getUserList().subscribe((respUserList: User[]) => {
      this.userList = respUserList;
    });
  }

  public getCurrentUser() {
    return this.api.callGetRoute<User>(this.prefix + '/' + this.currentUserToken);
  }

  public getUserList() {
    return this.api.callGetRoute<User[]>(this.prefix + '/');
  }

  public getGroupList() {
    return this.api.callGetRoute<Group[]>('group/');
  }

  public getUser(publicID: number) {
    return this.api.callGetRoute<User>(this.prefix + '/' + publicID);
  }

  public findUser(publicID: number): User {
    return this.userList.find(id => id.public_id === publicID);
  }

  public getUserAsync(publicID: number) {
    return this.api.callAsyncGetRoute<User>(this.prefix + '/' + publicID).then(response => {
      return response;
    }).catch(this.api.handleErrorPromise);
  }


}
