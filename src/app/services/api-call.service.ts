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
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

const httpOptions = {
  headers: new HttpHeaders({
    'Content-Type': 'application/json'
  })
};

@Injectable({
  providedIn: 'root'
})
export class ApiCallService {

  hostAddress = 'localhost';
  hostPort = 4000;
  private readonly apiPrefix = 'rest';
  private readonly apiURL;

  constructor(private http: HttpClient) {
    this.apiURL = 'http://' + this.hostAddress + ':' + this.hostPort + '/' + this.apiPrefix + '/';
  }

  public callGetRoute<T>(route: string, params?: any): Observable<any> {
    return this.http.get<T>(this.apiURL + route, params);
  }

  public async callAsyncGetRoute<T>(route: string): Promise<T> {
    return await this.http.get<T>(this.apiURL + route).toPromise<T>();
  }

  public callPostRoute(route: string, data) {
    return this.http.post<any>(this.apiURL + route, data, httpOptions);
  }

  public callDeleteRoute<T>(route: string, params?: any): Observable<any> {
    if (window.confirm('Are you sure, you want to delete?')) {
      return this.http.delete<T>(this.apiURL + route, params);
    }
    return new Observable<any>();
  }

  public handleErrorPromise(error: Response | any) {
    console.error(error.message || error);
    return Promise.reject(error.message || error);
  }
}
