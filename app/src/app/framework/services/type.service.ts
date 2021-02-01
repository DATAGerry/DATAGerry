/*
* DATAGERRY - OpenSource Enterprise CMDB
* Copyright (C) 2019 - 2020 NETHINKS GmbH
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
import { CmdbType } from '../models/cmdb-type';
import { ApiCallService, ApiService, httpObserveOptions, HttpProtocolHelper } from '../../services/api-call.service';
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
import { ValidatorService } from '../../services/validator.service';
import { UserService } from '../../management/services/user.service';
import { AccessControlPermission } from '../../acl/acl.types';


export const checkTypeExistsValidator = (typeService: TypeService, time: number = 500) => {
  return (control: FormControl) => {
    return timer(time).pipe(switchMap(() => {
      return typeService.getTypeByName(control.value).pipe(
        map((response) => {
          if (response === null) {
            return null;
          } else {
            return { typeExists: true };
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

  public servicePrefix: string = 'types';

  constructor(private api: ApiCallService, private userService: UserService) {
  }

  /**
   * Returns acl read filter
   *
   * @public
   */
  public getAclFilter(aclRequirement: AccessControlPermission | AccessControlPermission[] = AccessControlPermission.READ) {
    aclRequirement = Array.isArray(aclRequirement) ? aclRequirement : [aclRequirement];
    const location = 'acl.groups.includes.' + this.userService.getCurrentUser().group_id;
    return {
      $or: [
        { $or : [{acl: { $exists: false }}, {'acl.activated' : false}]},
        { $and : [
            {'acl.activated' : true},
            {$and : [
                { [location] : { $exists: true }},
                { [location] : { $all : aclRequirement}}
              ]},
          ]}]
    };
  }

  /**
   * Iterate over the type collection
   * @param params Instance of CollectionParameters
   */
  public getTypes(params: CollectionParameters = {
    filter: undefined,
    limit: 10,
    sort: 'public_id',
    order: 1,
    page: 1
  }): Observable<APIGetMultiResponse<T>> {
    const options = httpObserveOptions;
    let httpParams: HttpParams = new HttpParams();
    if (params.filter !== undefined) {
      const filter = JSON.stringify(params.filter);
      httpParams = httpParams.set('filter', filter);
    }
    httpParams = httpParams.set('limit', params.limit.toString());
    httpParams = httpParams.set('sort', params.sort);
    httpParams = httpParams.set('order', params.order.toString());
    httpParams = httpParams.set('page', params.page.toString());
    options.params = httpParams;
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
    const options = httpObserveOptions;
    options.params = new HttpParams();
    return this.api.callGet<CmdbType>(this.servicePrefix + '/' + publicID, options).pipe(
      map((apiResponse: HttpResponse<APIGetSingleResponse<T>>) => {
        return apiResponse.body.result as T;
      })
    );
  }

  /**
   * Get the complete type list
   */
  public getTypeList(aclRequirement?: AccessControlPermission | AccessControlPermission[]):
    Observable<Array<T>> {
    const options = httpObserveOptions;
    let params = new HttpParams();
    params = params.set('limit', '0');
    params = params.set('filter', JSON.stringify(this.getAclFilter(aclRequirement)));
    options.params = params;
    return this.api.callGet<Array<T>>(this.servicePrefix + '/', options).pipe(
      map((apiResponse: HttpResponse<APIGetMultiResponse<T>>) => {
        return apiResponse.body.results as Array<T>;
      })
    );
  }

  /**
   * Get types by the name or label
   * @param name Name of the type
   */
  public getTypeByName(name: string): Observable<T> {
    const options = httpObserveOptions;
    const filter = { name };
    let params: HttpParams = new HttpParams();
    params = params.set('filter', JSON.stringify(filter));
    options.params = params;
    return this.api.callGet<Array<T>>(this.servicePrefix + '/', options).pipe(
      map((apiResponse: HttpResponse<APIGetMultiResponse<T>>) => {
        if (apiResponse.body.count === 0) {
          return null;
        }
        return apiResponse.body.results[0] as T;
      })
    );
  }

  /**
   * Get types by the name or label
   * @param name Name/Label of the type
   * @param aclRequirements
   */
  public getTypesByNameOrLabel(name: string, aclRequirements?: AccessControlPermission | AccessControlPermission[]):
    Observable<Array<T>> {
    const regex = ValidatorService.validateRegex(name).trim();
    const filter = { $and : [{
      $or: [{ name: { $regex: regex, $options: 'ism' } }, { label: { $regex: regex, $options: 'ism' } }]
    },
        this.getAclFilter(aclRequirements)
      ]};
    const options = HttpProtocolHelper.createHttpProtocolOptions(httpObserveOptions, JSON.stringify(filter), 0);
    return this.api.callGet<Array<T>>(this.servicePrefix + '/', options).pipe(
      map((apiResponse: HttpResponse<APIGetMultiResponse<T>>) => {
        return apiResponse.body.results as Array<T>;
      })
    );
  }

  /**
   * Insert a new type into the database.
   */
  public postType(type: CmdbType): Observable<T> {
    const options = httpObserveOptions;
    options.params = new HttpParams();
    return this.api.callPost<T>(this.servicePrefix + '/', type, options).pipe(
      map((apiResponse: HttpResponse<APIInsertSingleResponse<T>>) => {
        return apiResponse.body.raw as T;
      })
    );
  }

  /**
   * Update a existing type in the database.
   */
  public putType(type: CmdbType): Observable<T> {
    const options = httpObserveOptions;
    options.params = new HttpParams();
    return this.api.callPut<T>(this.servicePrefix + '/' + type.public_id, type, options).pipe(
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
    const options = httpObserveOptions;
    options.params = new HttpParams();
    return this.api.callDelete<number>(this.servicePrefix + '/' + publicID, options).pipe(
      map((apiResponse: HttpResponse<APIDeleteSingleResponse<T>>) => {
        return apiResponse.body.raw as T;
      })
    );
  }

  /**
   * Get all uncategorized types
   */
  public getUncategorizedTypes(aclRequirements?: AccessControlPermission | AccessControlPermission[]):
    Observable<APIGetMultiResponse<T>> {
    const pipeline = [
      { $match: this.getAclFilter(aclRequirements) },
      { $lookup: { from: 'framework.categories', localField: 'public_id', foreignField: 'types', as: 'categories' } },
      { $match: { categories: { $size: 0 } } },
      { $project: { categories: 0 } }
    ];
    const options = HttpProtocolHelper.createHttpProtocolOptions(httpObserveOptions, JSON.stringify(pipeline), 0);
    return this.api.callGet<T[]>(this.servicePrefix  + '/', options).pipe(
      map((apiResponse: HttpResponse<APIGetMultiResponse<T>>) => {
        return apiResponse.body as APIGetMultiResponse<T>;
      })
    );
  }

  /**
   * Get a list of types by the category
   * @param categoryID PublicID of the category
   * @param aclRequirements
   */
  public getTypeListByCategory(categoryID: number, aclRequirements?: AccessControlPermission | AccessControlPermission[]):
    Observable<Array<T>> {
    const pipeline = [
      {
        $lookup: {
          from: 'framework.categories',
          let: { type_id: { $toInt: '$public_id' } },
          pipeline: [{ $match: { public_id: categoryID } }, { $match: { $expr: { $in: ['$$type_id', '$types'] } } }],
          as: 'category'
        }
      },
      { $match: { $and: [{ category: { $gt: { $size: 0 } } },
            this.getAclFilter(aclRequirements)
          ] }},
      { $project: { category: 0 } }
    ];
    const options = HttpProtocolHelper.createHttpProtocolOptions(httpObserveOptions, JSON.stringify(pipeline), 0);
    return this.api.callGet<Array<T>>(this.servicePrefix  + '/', options).pipe(
      map((apiResponse: HttpResponse<APIGetMultiResponse<T>>) => {
        return apiResponse.body.results as Array<T>;
      })
    );
  }

  /**
   * Get the total number of types in the system.
   */
  public countTypes(): Observable<number> {
    const options = httpObserveOptions;
    options.params = new HttpParams();
    return this.api.callHead<T[]>(this.servicePrefix + '/', options).pipe(
      map((apiResponse: HttpResponse<APIGetMultiResponse<T>>) => {
        return +apiResponse.headers.get('X-Total-Count');
      })
    );
  }

}

