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
import { HttpClient, HttpHeaders, HttpParams, HttpResponse } from '@angular/common/http';
import { APIGetMultiResponse, APIGetSingleResponse } from '../../services/models/api-response';

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
      return typeService.getTypeByName(control.value).pipe(
        map((response) => {
          if (response === null) {
            return null;
          } else {
            return { categoryExists: true };
          }
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

  constructor(private api: ApiCallService, private client: HttpClient) {
  }

  public getTypeIteration(...options): Observable<APIGetMultiResponse<T>> {
    let params: HttpParams = new HttpParams();
    for (const option of options) {
      for (const key of Object.keys(option)) {
        params = params.append(key, option[key]);
      }
    }
    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json'
      }),
      params,
      observe: resp
    };
    return this.api.callGet<T[]>(this.servicePrefix + '/', this.client, httpOptions).pipe(
      map((apiResponse: HttpResponse<APIGetMultiResponse<T>>) => {
        return apiResponse.body;
      })
    );
  }

  public getType(publicID: number): Observable<T> | undefined {
    return this.api.callGet<T>(this.servicePrefix + '/' + publicID).pipe(
      map((apiResponse: HttpResponse<APIGetSingleResponse<T>>) => {
        if (apiResponse.status === 204) {
          return undefined;
        }
        return apiResponse.body.result as T;
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

  /**
   * Get a type by name
   * @param type name or label of the type
   */
  public getTypeByName(type: string): Observable<T | null> {
    const params = encodeURIComponent(`{"name": "${ type }"}`);
    return this.api.callGet<T>(this.servicePrefix + `/?filter=` + params, this.client).pipe(
      map((apiResponse: HttpResponse<APIGetMultiResponse<T>>) => {
        if (apiResponse.body.count === 0) {
          return null;
        } else {
          return apiResponse.body.results[0];
        }
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

  public getUncategorizedTypes(): Observable<Array<T>> {
    // UNUSED FOR NOW
    return this.api.callGet<T>(this.servicePrefix + `/`, this.client).pipe(
      map((apiResponse: HttpResponse<APIGetMultiResponse<T>>) => {
        return [];
      })
    );
  }

  public getTypeListByCategory(publicID: number): Observable<any> {
    // UNUSED FOR NOW
    return this.api.callGet<T>(this.servicePrefix + `/`, this.client).pipe(
      map((apiResponse: HttpResponse<APIGetMultiResponse<T>>) => {
        return [];
      })
    );
  }

  public countTypes(): Observable<any> {
    // UNUSED FOR NOW
    return this.api.callGet<T>(this.servicePrefix + `/`, this.client).pipe(
      map((apiResponse: HttpResponse<APIGetMultiResponse<T>>) => {
        return 0;
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

}

