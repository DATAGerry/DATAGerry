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
import { CmdbType } from '../models/cmdb-type';
import { ApiCallService, ApiService, HttpInterceptorHandler, resp } from '../../services/api-call.service';
import { ValidatorService } from '../../services/validator.service';
import { Observable, timer } from 'rxjs';
import { catchError, map, switchMap } from 'rxjs/operators';
import { FormControl } from '@angular/forms';
import { HttpBackend, HttpClient, HttpHeaders } from '@angular/common/http';
import { BasicAuthInterceptor } from '../../auth/interceptors/basic-auth.interceptor';
import { AuthService } from '../../auth/services/auth.service';

export const httpObserveOptions = {
  headers: new HttpHeaders({
    'Content-Type': 'application/json'
  }),
  observe: resp
};

export const PARAMETER = 'params';
export const COOCKIENAME = 'onlyActiveObjCookie';

export const checkTypeExistsValidator = (typeService: TypeService<CmdbType>, time: number = 500) => {
  return (control: FormControl) => {
    return timer(time).pipe(switchMap(() => {
      return typeService.checkTypeExists(control.value).pipe(
        map(() => {
          return { typeExists: true };
        }),
        catchError(() => {
          return new Promise(resolve => {
            resolve(null);
          });
        })
      );
    }));
  };
};

@Injectable({
  providedIn: 'root'
})
export class TypeService<T = CmdbType> implements ApiService {

  public servicePrefix: string = 'type';
  private typeList: T[];

  constructor(private api: ApiCallService, private backend: HttpBackend,
              private authService: AuthService, private http: HttpClient) {
    // STRUCTURE IS DEPRECATED PLEASE NOT USE
    this.getTypeList().subscribe((respTypeList: T[]) => {
      this.typeList = respTypeList;
    });
  }

  public findType(publicID: number): T {
    // FUNCTION IS DEPRECATED PLEASE NOT USE
    // @ts-ignore
    return this.typeList.find(id => id.public_id === publicID);
  }

  public getType(publicID: number): Observable<T> {
    return this.api.callGet<CmdbType>(this.servicePrefix + '/' + publicID).pipe(
      map((apiResponse) => {
        return apiResponse.body;
      })
    );
  }

  public getTypeList(): Observable<T[]> {
    return this.api.callGet<CmdbType[]>(this.servicePrefix + '/').pipe(
      map((apiResponse) => {
        return apiResponse.body;
      })
    );
  }

  public getTypesBy(regex: string): Observable<T[]> {
    regex = ValidatorService.validateRegex(regex).trim();
    return this.api.callGet<CmdbType[]>(this.servicePrefix + '/find/' + encodeURIComponent(regex)).pipe(
      map((apiResponse) => {
        return apiResponse.body;
      })
    );
  }

  public postType(typeInstance: CmdbType): Observable<any> {
    return this.api.callPost<T>(this.servicePrefix + '/', typeInstance).pipe(
      map((apiResponse) => {
        return apiResponse.body;
      })
    );
  }

  public putType(typeInstance: CmdbType): Observable<any> {
    return this.api.callPut<T>(this.servicePrefix + '/', typeInstance).pipe(
      map((apiResponse) => {
        return apiResponse.body;
      })
    );
  }

  public deleteType(publicID: number): Observable<any> {
    return this.api.callDelete<number>(this.servicePrefix + '/' + publicID).pipe(
      map((apiResponse) => {
        return apiResponse.body;
      })
    );
  }

  public getUncategorizedTypes(): Observable<any> {
    return this.api.callGet<T[]>(this.servicePrefix + '/uncategorized/', this.http, httpObserveOptions).pipe(
      map((apiResponse) => {
        return apiResponse.body;
      })
    );
  }

  public getTypeListByCategory(publicID: number): Observable<any> {
    return this.api.callGet<T[]>(this.servicePrefix + '/category/' + publicID).pipe(
      map((apiResponse) => {
        if (apiResponse.status === 204) {
          return [];
        }
        return apiResponse.body;
      })
    );
  }

  public countTypes(): Observable<any> {
    return this.api.callGet<T[]>(this.servicePrefix + '/count/').pipe(
      map((apiResponse) => {
        return apiResponse.body;
      })
    );
  }

  public cleanupRemovedFields(publicID: number): Observable<any> {
    return this.api.callGet(this.servicePrefix + '/cleanup/remove/' + publicID).pipe(
      map((apiResponse) => {
        if (apiResponse.status === 204) {
          return [];
        }
        return apiResponse.body;
      })
    );
  }

  public cleanupInsertedFields(publicID: number): Observable<any> {
    return this.api.callGet(this.servicePrefix + '/cleanup/update/' + publicID).pipe(
      map((apiResponse) => {
        if (apiResponse.status === 204) {
          return [];
        }
        return apiResponse.body;
      })
    );
  }

  // Validation functions
  public checkTypeExists(typeName: string) {
    const specialClient = new HttpClient(new HttpInterceptorHandler(this.backend, new BasicAuthInterceptor()));
    return this.api.callGet<T>(`${ this.servicePrefix }/${ typeName }`, specialClient);
  }
}

