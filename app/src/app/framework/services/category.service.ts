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
* along with this program. If not, see <https://www.gnu.org/licenses/>.
*/

import { Injectable } from '@angular/core';
import { catchError, map, switchMap } from 'rxjs/operators';
import { ApiCallService, ApiService, resp } from '../../services/api-call.service';
import { ValidatorService } from '../../services/validator.service';
import { CmdbCategory, CmdbCategoryNode, CmdbCategoryTree } from '../models/cmdb-category';
import { FormControl } from '@angular/forms';
import { Observable, timer } from 'rxjs';
import { HttpClient, HttpHeaders, HttpParams, HttpResponse } from '@angular/common/http';
import { APIGetMultiResponse, APIGetSingleResponse } from '../../services/models/api-response';

export const checkCategoryExistsValidator = (categoryService: CategoryService, time: number = 500) => {
  return (control: FormControl) => {
    return timer(time).pipe(switchMap(() => {
      return categoryService.getCategoryByName(control.value).pipe(
        map((response) => {
          return { categoryExists: true };
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
export class CategoryService<T = CmdbCategory> implements ApiService {

  /**
   * Nested url path value inside the REST structure
   */
  public servicePrefix: string = 'categories';

  constructor(private api: ApiCallService, private client: HttpClient) {

  }

  public getCategoryIteration(...options): Observable<APIGetMultiResponse<T>> {
    let params: HttpParams = new HttpParams();
    for (const option of options) {
      for (const key of Object.keys(option)) {
        params = params.append(key, option[key]);
      }
    }
    const httpObserveOptions = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json'
      }),
      params,
      observe: resp
    };
    return this.api.callGet<T[]>(this.servicePrefix + '/', this.client, httpObserveOptions).pipe(
      map((apiResponse: HttpResponse<APIGetMultiResponse<T>>) => {
        return apiResponse.body;
      })
    );
  }

  /**
   * Get all categories as a list
   */
  public getCategoryList(): Observable<T[]> {
    return this.api.callGet<T[]>(this.servicePrefix + '/?limit=1000').pipe(
      map((apiResponse: HttpResponse<APIGetMultiResponse<T>>) => {
        if (apiResponse.status === 204) {
          return [];
        }
        return apiResponse.body.results;
      })
    );
  }

  /**
   * Get a category by id
   */
  public getCategory(publicID: number): Observable<T> | undefined {
    return this.api.callGet<T>(this.servicePrefix + '/' + publicID).pipe(
      map((apiResponse: HttpResponse<APIGetSingleResponse<T>>) => {
        if (apiResponse.status === 204) {
          return undefined;
        }
        return apiResponse.body.result;
      })
    );
  }

  /**
   * Get a category by name
   * @param category name or label of the category
   */
  public getCategoryByName(category: string): Observable<T | null> {
    return this.api.callGet<T>(this.servicePrefix + '/' + category).pipe(
      map((apiResponse: HttpResponse<T>) => {
        if (apiResponse.status === 204) {
          return null;
        }
        return apiResponse.body;
      })
    );
  }

  /**
   * Get a list of categories by a regex requirement
   * Works with name and label
   * @param regex parameter
   */
  public getCategoriesByName(regex: string): Observable<T[]> {
    regex = ValidatorService.validateRegex(regex).trim();
    return this.api.callGet<T[]>(this.servicePrefix + '/find/' + encodeURIComponent(regex)).pipe(
      map((apiResponse: HttpResponse<T[]>) => {
        if (apiResponse.status === 204) {
          return [];
        }
        return apiResponse.body;
      })
    );
  }


  /**
   * Get the complete category tree with
   * nested structure and type instances
   */
  public getCategoryTree(): Observable<CmdbCategoryTree> {
    return this.api.callGet<CmdbCategoryTree>(`${ this.servicePrefix }/?view=tree`).pipe(
      map((apiResponse: HttpResponse<APIGetMultiResponse<CmdbCategoryNode>>) => {
        if (apiResponse.status === 204) {
          return [];
        }
        return apiResponse.body.results as CmdbCategoryTree;
      })
    );
  }

  /**
   * Add a new unique category into the database
   * @param category raw instance of a CategoryDAO
   */
  public postCategory(category: T): Observable<T> {
    return this.api.callPost<CmdbCategory>(this.servicePrefix + '/', category).pipe(
      map((apiResponse: HttpResponse<any>) => {
        if (apiResponse.status === 204) {
          return [];
        }
        return apiResponse.body;
      })
    );
  }

  /**
   * Update a existing category
   * @param category modified category instance
   */
  public updateCategory(category: T): Observable<T> {
    return this.api.callPut<number>(this.servicePrefix + '/', category).pipe(
      map((apiResponse: HttpResponse<T>) => {
        return apiResponse.body;
      })
    );
  }


  /**
   * Delete a existing category
   * @param publicID the category id
   */
  public deleteCategory(publicID: number): Observable<number> {
    return this.api.callDelete<number>(this.servicePrefix + '/' + publicID).pipe(
      map((apiResponse: HttpResponse<number>) => {
        return apiResponse.body;
      })
    );
  }

}
