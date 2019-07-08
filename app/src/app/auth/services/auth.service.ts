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
import { BehaviorSubject, Observable } from 'rxjs';
import { UserToken } from '../models/user-token';
import { map } from 'rxjs/operators';
import { HttpClient, HttpHeaders } from '@angular/common/http';

const httpOptions = {
  headers: new HttpHeaders({
    'Content-Type': 'application/json'
  })
};


@Injectable({
  providedIn: 'root'
})
export class AuthService {

  private restPrefix: string = 'rest';
  private servicePrefix: string = 'auth';
  private currentUserSubject: BehaviorSubject<UserToken>;
  public currentUser: Observable<UserToken>;

  constructor(private http: HttpClient) {
    this.currentUserSubject = new BehaviorSubject<UserToken>(JSON.parse(localStorage.getItem('access-token')));
    this.currentUser = this.currentUserSubject.asObservable();
  }

  public get currentUserValue(): UserToken {
    return this.currentUserSubject.value;
  }

  public login(username: string, password: string) {
    console.log(username);
    console.log(password);
    const data = {
      user_name: username,
      password
    };
    return this.http.post<UserToken>(`http://localhost:4000/${this.restPrefix}/${this.servicePrefix}/login`, data, httpOptions)
      .pipe(map(userToken => {
        console.log(userToken);
        // store user details and jwt token in local storage to keep user logged in between page refreshes
        localStorage.setItem('access-token', JSON.stringify(userToken));
        this.currentUserSubject.next(userToken);
        return userToken;
      }));
  }

  public logout() {
    localStorage.removeItem('access-token');
    this.currentUserSubject.next(null);
  }
}
