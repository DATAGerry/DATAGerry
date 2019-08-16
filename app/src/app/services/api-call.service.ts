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
import { ConnectionService } from './connection.service';

const httpOptions = {
  headers: new HttpHeaders({
    'Content-Type': 'application/json'
  })
};

@Injectable({
  providedIn: 'root'
})
export class ApiCallService {

  private readonly apiPrefix = 'rest';
  private readonly apiURL;

  constructor(private http: HttpClient, private connectionService: ConnectionService) {
    this.apiURL = `${this.connectionService.connectionURL}${this.apiPrefix}/`;
  }

  public callGetRoute<T>(route: string, params?: any): Observable<any> {
    return this.http.get<T>(this.apiURL + route, params);
  }

  public async callAsyncGetRoute<T>(route: string): Promise<T> {
    return await this.http.get<T>(this.apiURL + route).toPromise<T>();
  }

  public callPostRoute<T>(route: string, data, options: any = httpOptions) {
    return this.http.post<T>(this.apiURL + route, data, options);
  }

  public callPutRoute<T>(route: string, data) {
    return this.http.put<T>(this.apiURL + route, data, httpOptions);
  }

  public callDeleteManyRoute<T>(route: string, params?: any): Observable<any> {
      return this.http.get<T>(this.apiURL + route, params);
  }

  public callDeleteRoute<T>(route: string, params?: any): Observable<any> {
    return this.http.delete<T>(this.apiURL + route, params);
  }

  public handleErrorPromise(error: Response | any) {
    console.error(error.message || error);
    return Promise.reject(error.message || error);
  }
}
