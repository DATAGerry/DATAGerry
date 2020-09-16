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
import { ApiCallService, ApiService, httpObserveOptions } from '../../services/api-call.service';
import { Observable, timer } from 'rxjs';
import { catchError, map, switchMap } from 'rxjs/operators';
import { FormControl } from '@angular/forms';
import { HttpParams, HttpResponse } from '@angular/common/http';
import {
  APIDeleteSingleResponse,
  APIGetMultiResponse,
  APIGetSingleResponse,
  APIInsertSingleResponse,
  APIUpdateSingleResponse
} from '../../services/models/api-response';
import { CollectionParameters } from '../../services/models/api-parameter';


export const checkTypeExistsValidator = (typeService: TypeService, time: number = 500) => {
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

  constructor(private api: ApiCallService) {
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

    return this.api.callGet<Array<T>>(this.servicePrefix + '/', options).pipe(
      map((apiResponse: HttpResponse<APIGetMultiResponse<T>>) => {
        return apiResponse.body;
      })
    );
  }

  /**
   * Get a specific type by the id
   * @param publicID PublicID of the type
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
    return this.api.callGet<Array<T>>(this.servicePrefix + '/?limit=0').pipe(
      map((apiResponse: HttpResponse<APIGetMultiResponse<T>>) => {
        return apiResponse.body.results as Array<T>;
      })
    );
  }

  /**
   * Get types by the name or label
   * @param name Name or Label of the type
   */
  public getTypesByName(name: string): Observable<Array<T>> {
    const options = httpObserveOptions;
    const filter = {
      $or: [{ name: { $regex: name, $options: 'ismx' } }, { label: { $regex: name, $options: 'ismx' } }]
    };
    let params: HttpParams = new HttpParams();
    params = params.set('filter', JSON.stringify(filter));
    params = params.set('limit', '0');
    options.params = params;
    return this.api.callGet<Array<T>>(this.servicePrefix + '/', options).pipe(
      map((apiResponse: HttpResponse<APIGetMultiResponse<T>>) => {
        return apiResponse.body.results as Array<T>;
      })
    );
  }

  /**
   * Insert a new type into the database.
   */
  public postType(typeInstance: CmdbType): Observable<T> {
    return this.api.callPost<T>(this.servicePrefix + '/', typeInstance).pipe(
      map((apiResponse: HttpResponse<APIInsertSingleResponse<T>>) => {
        return apiResponse.body.raw as T;
      })
    );
  }

  /**
   * Update a existing type in the database.
   */
  public putType(typeInstance: CmdbType): Observable<T> {
    return this.api.callPut<T>(this.servicePrefix + '/', typeInstance).pipe(
      map((apiResponse: HttpResponse<APIUpdateSingleResponse<T>>) => {
        return apiResponse.body.result as T;
      })
    );
  }

  /**
   * Delete a existing type in the database.
   * @returns The deleted type instance.
   */
  public deleteType(publicID: number): Observable<T> {
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
      { $lookup: { from: 'framework.categories', localField: 'public_id', foreignField: 'types', as: 'categories' } },
      { $match: { categories: { $size: 0 } } },
      { $project: { categories: 0 } }
    ];

    const filter = JSON.stringify(pipeline);
    return this.api.callGet<Array<T>>(this.servicePrefix + `/?filter=${ filter }&limit=0`).pipe(
      map((apiResponse: HttpResponse<APIGetMultiResponse<T>>) => {
        return apiResponse.body as APIGetMultiResponse<T>;
      })
    );
  }

  /**
   * Get a list of types by the category
   * @param categoryID PublicID of the category
   */
  public getTypeListByCategory(categoryID: number): Observable<Array<T>> {
    const pipeline = [
      {
        $lookup: {
          from: 'framework.categories',
          let: { type_id: { $toInt: '$public_id' } },
          pipeline: [{ $match: { public_id: categoryID } }, { $match: { $expr: { $in: ['$$type_id', '$types'] } } }],
          as: 'category'
        }
      },
      { $match: { category: { $gt: { $size: 0 } } } },
      { $project: { category: 0 } }
    ];
    const filter = JSON.stringify(pipeline);
    return this.api.callGet<T[]>(this.servicePrefix + `/?filter=${ filter }&limit=0`).pipe(
      map((apiResponse: HttpResponse<APIGetMultiResponse<T>>) => {
        return apiResponse.body.results as Array<T>;
      })
    );
  }

  /**
   * Get the total number of types in the system.
   */
  public countTypes(): Observable<number> {
    return this.api.callHead<T[]>(this.servicePrefix + '/').pipe(
      map((apiResponse: HttpResponse<APIGetMultiResponse<T>>) => {
        console.log(apiResponse.headers);
        return +apiResponse.headers.get('X-Total-Count');
      })
    );
  }

}

