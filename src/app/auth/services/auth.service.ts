/*
* Net|CMDB - OpenSource Enterprise CMDB
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
import { BehaviorSubject, Observable } from 'rxjs';
import { UserToken } from '../models/user-token';


@Injectable({
  providedIn: 'root'
})
export class AuthService {

  private currentUserSubject: BehaviorSubject<UserToken>;
  public currentUser: Observable<UserToken>;

  constructor(private api: ApiCallService) {
    this.currentUserSubject = new BehaviorSubject<UserToken>(JSON.parse(localStorage.getItem('access-token')));
    this.currentUser = this.currentUserSubject.asObservable();
  }

  public get currentUserValue(): UserToken {
    return this.currentUserSubject.value;
  }


  public login(userName: string, userPassword: string) {
    const data = {
      user_name: userName,
      password: userPassword
    };
    const apiResponse = this.api.callPostRoute('auth/login', data);

    apiResponse.subscribe((loginResponse: any) => {
        localStorage.setItem('access-token', JSON.stringify(loginResponse));
        this.currentUserSubject.next(loginResponse);
      }
    );

    return apiResponse;

  }

  public logout() {
    localStorage.removeItem('access-token');
    this.currentUserSubject.next(null);
  }
}
