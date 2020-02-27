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
import {catchError, map, switchMap} from 'rxjs/operators';
import {ApiCallService, ApiService, HttpInterceptorHandler} from '../../services/api-call.service';
import { CmdbCategory } from '../models/cmdb-category';
import { FormControl } from '@angular/forms';
import { Observable, timer } from 'rxjs';
import {HttpBackend, HttpClient} from '@angular/common/http';
import { BasicAuthInterceptor } from '../../auth/interceptors/basic-auth.interceptor';

export const checkCategoryExistsValidator = (categoryService: CategoryService<CmdbCategory>, time: number = 500) => {
  return (control: FormControl) => {
    return timer(time).pipe(switchMap(() => {
      return categoryService.checkCategoryExists(control.value).pipe(
        map((response) => {
          if (response.body.length) {
            return { typeExists: true };
          }
          return null;
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

  public servicePrefix: string = 'category';
  private categoryList: CmdbCategory[];

  constructor(private api: ApiCallService, private backend: HttpBackend) {
    this.getCategoryList().subscribe((list: CmdbCategory[]) => {
      this.categoryList = list;
    });
  }

  public findCategory(publicID: number): CmdbCategory {
    return this.categoryList.find(category => category.public_id === publicID);
  }

  public getCategory(publicID: number) {
    return this.api.callGet<CmdbCategory>(this.servicePrefix + '/' + publicID).pipe(
      map((apiResponse) => {
        if (apiResponse.status === 204) {
          return [];
        }
        return apiResponse.body;
      })
    );
  }

  public getCategoriesBy(regex: string): Observable<T[]> {
    return this.api.callGet<CmdbCategory[]>(this.servicePrefix + '/by/' + regex).pipe(
      map((apiResponse) => {
        return apiResponse.body;
      })
    );
  }

  public getRootCategory() {
    return this.api.callGet<CmdbCategory>(this.servicePrefix + '/root/').pipe(
      map((apiResponse) => {
        if (apiResponse.status === 204) {
          return [];
        }
        return apiResponse.body;
      })
    );
  }

  public getCategoryList() {
    return this.api.callGet<CmdbCategory[]>(this.servicePrefix + '/').pipe(
      map((apiResponse) => {
        if (apiResponse.status === 204) {
          return [];
        }
        return apiResponse.body;
      })
    );
  }

  public getCategoryTree() {
    return this.api.callGet<CmdbCategory[]>(this.servicePrefix + '/tree').pipe(
      map((apiResponse) => {
        if (apiResponse.status === 204) {
          return [];
        }
        return apiResponse.body;
      })
    );
  }

  public postCategory(data: CmdbCategory) {
    return this.api.callPostRoute<CmdbCategory>(this.servicePrefix + '/', data);
  }

  public updateCategory(data) {
    return this.api.callPutRoute<number>(this.servicePrefix + '/', data);
  }

  public deleteCategory(publicID: number) {
    return this.api.callDeleteRoute<number>(this.servicePrefix + '/' + publicID);
  }

  // Validation functions
  public checkCategoryExists(typeName: string) {
    const specialClient = new HttpClient(new HttpInterceptorHandler(this.backend, new BasicAuthInterceptor()));
    return this.api.callGet<T>(`${ this.servicePrefix }/${ typeName }`, specialClient);
  }
}
