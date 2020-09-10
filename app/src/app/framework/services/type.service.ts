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
import { ApiCallService, ApiService, resp } from '../../services/api-call.service';
import { Observable, timer } from 'rxjs';
import { catchError, map, switchMap } from 'rxjs/operators';
import { FormControl } from '@angular/forms';
import { HttpClient, HttpHeaders, HttpParams, HttpResponse } from '@angular/common/http';
import {
  APIDeleteSingleResponse,
  APIGetMultiResponse,
  APIGetSingleResponse,
  APIInsertSingleResponse,
  APIUpdateSingleResponse
} from '../../services/models/api-response';
import { CollectionParameters } from '../../services/models/api-parameter';

export const PARAMETER = 'params';
export const COOCKIENAME = 'onlyActiveObjCookie';

export const checkTypeExistsValidator = (typeService: TypeService<CmdbType>, time: number = 500) => {
  return (control: FormControl) => {
    return timer(time).pipe(switchMap(() => {
      return typeService.getTypesByName(control.value).pipe(
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

  public servicePrefix: string = 'types';

  constructor(private api: ApiCallService, private client: HttpClient) {
  }

  /**
   * Iterate over the type collection
   * @param options Instance of CollectionParameters
   */
  public getTypesIteration(options: CollectionParameters = {
    filter: undefined,
    limit: 10,
    sort: 'public_id',
    order: 1,
    page: 1
  }): Observable<APIGetMultiResponse<T>> {
    let params: HttpParams = new HttpParams();
    for (const key in options) {
      if (options.hasOwnProperty(key)) {
        params = params.set(key, options[key]);
      }
    }

    return this.api.callGet<T[]>(this.servicePrefix + '/', options).pipe(
      map((apiResponse: HttpResponse<APIGetMultiResponse<T>>) => {
        return apiResponse.body;
      })
    );
  }

  /**
   * Get a specific type by the id
   * @param publicID
   */
  public getType(publicID: number): Observable<T> {
    return this.api.callGet<CmdbType>(this.servicePrefix + '/' + publicID).pipe(
      map((apiResponse: HttpResponse<APIGetSingleResponse<T>>) => {
        return apiResponse.body.result as T;
      })
    );
  }

  /**
   * Get the complete type list
   */
  public getTypeList(): Observable<Array<T>> {
    return this.api.callGet<CmdbType[]>(this.servicePrefix + '/?limit=0').pipe(
      map((apiResponse: HttpResponse<APIGetMultiResponse<T>>) => {
        return apiResponse.body.results as Array<T>;
      })
    );
  }

  /**
   * Get types by the name or label
   * @param name
   */
  public getTypesByName(name: string): Observable<Array<T>> {
    const filter = {
      $or: [
        {
          name: { $regex: name, $options: 'ismx' }
        },
        {
          label: { $regex: name, $options: 'ismx' }
        }
      ]
    };
    let params: HttpParams = new HttpParams();

    params = params.set('filter', JSON.stringify(filter));
    params = params.set('limit', '0');
    return this.api.callGet<T[]>(this.servicePrefix + '/', params).pipe(
      map((apiResponse: HttpResponse<APIGetMultiResponse<T>>) => {
        return apiResponse.body.results as Array<T>;
      })
    );
  }


  public postType(typeInstance: CmdbType): Observable<T> {
    /**
     * Insert a new type into the database.
     */
    return this.api.callPost<T>(this.servicePrefix + '/', typeInstance).pipe(
      map((apiResponse: HttpResponse<APIInsertSingleResponse<T>>) => {
        return apiResponse.body.raw as T;
      })
    );
  }

  public putType(typeInstance: CmdbType): Observable<T> {
    /**
     * Update a existing type in the database.
     */
    return this.api.callPut<T>(this.servicePrefix + '/', typeInstance).pipe(
      map((apiResponse: HttpResponse<APIUpdateSingleResponse<T>>) => {
        return apiResponse.body.result as T;
      })
    );
  }

  public deleteType(publicID: number): Observable<T> {
    /**
     * Delete a existing type in the database.
     * @returns The deleted type instance.
     */
    return this.api.callDelete<number>(this.servicePrefix + '/' + publicID).pipe(
      map((apiResponse: HttpResponse<APIDeleteSingleResponse<T>>) => {
        return apiResponse.body.deleted_entry as T;
      })
    );
  }

  /**
   * Get all uncategorized types
   */
  public getUncategorizedTypes(): Observable<APIGetMultiResponse<T>> {
    const pipeline = [
      { $match: {} },
      {
        $lookup: {
          from: 'framework.categories',
          localField: 'public_id',
          foreignField: 'types',
          as: 'categories'
        }
      },
      {
        $match: { categories: { $size: 0 } }
      },
      { $project: { categories: 0 } }
    ];

    const filter = JSON.stringify(pipeline);
    return this.api.callGet<Array<T>>(this.servicePrefix + `/?filter=${ filter }&limit=0`).pipe(
      map((apiResponse: HttpResponse<APIGetMultiResponse<T>>) => {
        return apiResponse.body as APIGetMultiResponse<T>;
      })
    );
  }

  public getTypeListByCategory(publicID: number): Observable<Array<T>> {
    return this.api.callGet<T[]>(this.servicePrefix + '/' + publicID).pipe(
      map((apiResponse) => {
        if (apiResponse.status === 204) {
          return [];
        }
        return apiResponse.body.r;
      })
    );
  }

  public countTypes(): Observable<number> {
    /**
     * Get the total number of types in the system.
     */
    return this.api.callHead<T[]>(this.servicePrefix + '/').pipe(
      map((apiResponse: HttpResponse<APIGetMultiResponse<T>>) => {
        return +apiResponse.headers.get('X-Total-Count');
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

