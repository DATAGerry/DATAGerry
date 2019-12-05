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
import {
  HttpClient,
  HttpErrorResponse,
  HttpEvent,
  HttpHandler,
  HttpHeaders,
  HttpInterceptor, HttpRequest
} from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { map, catchError } from 'rxjs/operators';
import { ConnectionService } from '../connect/connection.service';

const httpOptions = {
  headers: new HttpHeaders({
    'Content-Type': 'application/json'
  })
};

declare type HttpObserve = 'body' | 'events' | 'response';
export const resp: HttpObserve = 'response';

export const httpObserveOptions = {
  headers: new HttpHeaders({
    'Content-Type': 'application/json'
  }),
  observe: resp
};

export const httpFileOptions = {
  headers: new HttpHeaders({}),
  params: {},
  observe: resp
};

@Injectable({
  providedIn: 'root'
})
export class ApiCallService {

  private readonly apiPrefix = 'rest';
  private readonly apiURL;

  public static handleError(err: HttpErrorResponse) {
    if (err.error instanceof ErrorEvent) {
      console.error('An error occurred:', err.error.message);
    } else {
      console.error(
        `Backend returned code ${ err.status }, ` +
        `body was: ${ err.error }`);
    }
    return throwError(err);
  }

  constructor(private http: HttpClient, private connectionService: ConnectionService) {
    this.apiURL = `${ this.connectionService.currentConnection }/${ this.apiPrefix }/`;
  }

  public callGet<T>(route: string, client: HttpClient = this.http): Observable<any> {
    return client.get<T>(this.apiURL + route, httpObserveOptions).pipe(catchError(ApiCallService.handleError));
  }

  public callPost<T>(route: string, data, httpPostOptions = httpObserveOptions): Observable<any> {
    return this.http.post<T>(this.apiURL + route, data, httpPostOptions).pipe(catchError(ApiCallService.handleError));
  }

  public callPut<T>(route: string, data): Observable<any> {
    return this.http.put<T>(this.apiURL + route, data, httpObserveOptions).pipe(catchError(ApiCallService.handleError));
  }

  public callDelete<T>(route: string, httpDeleteOptions = httpObserveOptions): Observable<any> {
    return this.http.delete<T>(this.apiURL + route, httpDeleteOptions).pipe(catchError(ApiCallService.handleError));
  }

  /* DEPRECATED API METHODS - ONLY USE TOP METHODS */

  public callGetRoute<T>(route: string, params?: any): Observable<any> {
    return this.http.get<T>(this.apiURL + route, params).pipe(
      map((res) => {
        return res;
      }),
      catchError(ApiCallService.handleError)
    );
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

}

export interface ApiService {
  servicePrefix: string;
}

export class HttpInterceptorHandler implements HttpHandler {
  constructor(private next: HttpHandler, private interceptor: HttpInterceptor) {
  }

  handle(req: HttpRequest<any>): Observable<HttpEvent<any>> {
    return this.interceptor.intercept(req, this.next);
  }
}
