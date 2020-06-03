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
import { ApiCallService, ApiService } from '../../services/api-call.service';
import { ValidatorService } from '../../services/validator.service';
import { CmdbCategory, CmdbCategoryTree } from '../models/cmdb-category';
import { FormControl } from '@angular/forms';
import { Observable, timer } from 'rxjs';
import { HttpResponse } from '@angular/common/http';

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
   * Fixed URL extension
   * Nested url path value inside the REST structure
   */
  public servicePrefix: string = 'category';

  constructor(private api: ApiCallService) {

  }

  /**
   * Get a category by id
   */
  public getCategory(publicID: number): Observable<T | null> {
    return this.api.callGet<T>(this.servicePrefix + '/' + publicID).pipe(
      map((apiResponse: HttpResponse<T>) => {
        if (apiResponse.status === 204) {
          return null;
        }
        return apiResponse.body;
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
   * Get all categories as a list
   */
  public getCategoryList(): Observable<T[]> {
    return this.api.callGet<T[]>(this.servicePrefix + '/').pipe(
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
  public getCategoryTree(): Observable<CmdbCategoryTree | null> {
    return this.api.callGet<CmdbCategoryTree>(this.servicePrefix + '/tree/').pipe(
      map((apiResponse: HttpResponse<CmdbCategoryTree>) => {
        if (apiResponse.status === 204) {
          return null;
        }
        return apiResponse.body;
      })
    );
  }

  /**
   * Add a new unique category into the database
   * @param data raw instance of a CmdbCategory
   */
  public postCategory(data: T): Observable<T> {
    return this.api.callPost<CmdbCategory>(this.servicePrefix + '/', data).pipe(
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
   * @param data modified category instance
   */
  public updateCategory(data: T): Observable<T> {
    return this.api.callPut<number>(this.servicePrefix + '/', data).pipe(
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
