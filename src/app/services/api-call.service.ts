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
import {HttpClient, HttpHeaders} from '@angular/common/http';
import {Observable} from 'rxjs';
import { map } from 'rxjs/operators';
import { debounceTime } from 'rxjs/internal/operators/debounceTime';

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


  public callGetRoute<T>(route: string): Observable<any> {
    return this.http.get<T>(this.apiURL + route);
  }

  public async callAsyncGetRoute<T>(route: string): Promise<T> {
    return this.http.get<T>(this.apiURL + route).toPromise<T>();
  }

  public callPostRoute(route: string, data) {
    return this.http.post<any>(this.apiURL + route, data, httpOptions);
  }

  public searchTerm(route: string) {
    let result = this.http.get(this.apiURL + route, {params: {limit: "5"}})
      .pipe(
        debounceTime(500),  // WAIT FOR 500 MILISECONDS ATER EACH KEY STROKE.
        map(
          (data: any) => {
            return (
              data.length > 0 ? data as any[] : [{"Object": "No Object Found"} as any]
            );
          }
        ));

    return result;
  }
}
