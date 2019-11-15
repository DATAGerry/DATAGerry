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

import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { ConnectionService } from '../../connect/connection.service';
import { User } from '../../management/models/user';
import { Right } from '../../management/models/right';
import { PermissionService } from './permission.service';

const httpOptions = {
  headers: new HttpHeaders({
    'Content-Type': 'application/json'
  })
};


@Injectable({
  providedIn: 'root'
})
export class AuthService {

  // Rest backend
  private restPrefix: string = 'rest';
  private servicePrefix: string = 'auth';

  // User storage
  private currentUserSubject: BehaviorSubject<User>;
  public currentUser: Observable<User>;
  private currentUserTokenSubject: BehaviorSubject<string>;
  public currentUserToken: Observable<string>;

  constructor(private http: HttpClient, private connectionService: ConnectionService,
              private permissionService: PermissionService) {
    this.currentUserSubject = new BehaviorSubject<User>(
      JSON.parse(localStorage.getItem('current-user')));
    this.currentUser = this.currentUserSubject.asObservable();

    this.currentUserTokenSubject = new BehaviorSubject<string>(
      JSON.parse(localStorage.getItem('access-token')));
    this.currentUserToken = this.currentUserTokenSubject.asObservable();
  }

  public get currentUserValue(): User {
    return this.currentUserSubject.value;
  }

  public get currentUserTokenValue(): string {
    return this.currentUserTokenSubject.value;
  }


  public getAuthProviders() {
    return this.http.get(`${ this.connectionService.currentConnection }/${ this.restPrefix }/${ this.servicePrefix }/providers`).pipe(
      map((apiResponse) => {
        return apiResponse;
      })
    );
  }

  public login(username: string, password: string) {
    const data = {
      user_name: username,
      password
    };
    return this.http.post<User>(
      `${ this.connectionService.currentConnection }/${ this.restPrefix }/${ this.servicePrefix }/login`, data, httpOptions)
      .pipe(map(user => {
        localStorage.setItem('current-user', JSON.stringify(user));
        localStorage.setItem('access-token', JSON.stringify(user.token));
        this.currentUserSubject.next(user);
        this.currentUserTokenSubject.next(user.token);
        this.permissionService.storeUserRights(user.group_id);
        return user;
      }));
  }

  public logout() {
    localStorage.removeItem('current-user');
    localStorage.removeItem('access-token');
    this.currentUserSubject.next(null);
    this.currentUserTokenSubject.next(null);
    this.permissionService.clearUserRightStorage();
  }
}
