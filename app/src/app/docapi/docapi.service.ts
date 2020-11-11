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

import { HttpInterceptorHandler, ApiCallService, ApiService, httpFileOptions } from '../services/api-call.service';
import { HttpBackend, HttpClient } from '@angular/common/http';
import { FormControl } from '@angular/forms';
import { switchMap, map, catchError } from 'rxjs/operators';
import { Observable, timer } from 'rxjs';
import { DocTemplate } from '../framework/models/cmdb-doctemplate';
import { BasicAuthInterceptor } from '../auth/interceptors/basic-auth.interceptor';



@Injectable({
  providedIn: 'root'
})
export class DocapiService<T = DocTemplate> implements ApiService {

  public readonly servicePrefix: string = 'docapi/template';

  constructor(private api: ApiCallService, private http: HttpClient, private backend: HttpBackend) {
  }

  getDocTemplateList(): Observable<T[]> {
    return this.api.callGet<T>(`${ this.servicePrefix }/`).pipe(
      map((apiResponse) => {
        if (apiResponse.status === 204) {
          return [];
        }
        return apiResponse.body;
      })
    );
  }


  getObjectDocTemplateList(typeId: number): Observable<T[]> {
    const searchfilter = {
      template_type: 'OBJECT',
      template_parameters: { type: typeId }
    };
    return this.api.callGet<T>(`${ this.servicePrefix }/by/${ JSON.stringify(searchfilter) }`).pipe(
      map((apiResponse) => {
        if (apiResponse.status === 204) {
          return [];
        }
        return apiResponse.body;
      })
    );
  }


  getRenderedObjectDoc(templateId: number, objectId: number) {
    return this.api.callGet<any>(`${ this.servicePrefix }/${ templateId }/render/${ objectId }`, httpFileOptions);
  }


  // CRUD calls
  public getDocTemplate(publicId: number) {
    return this.api.callGet<DocTemplate>(this.servicePrefix + '/' + publicId).pipe(
      map((apiResponse) => {
        if (apiResponse.status === 204) {
          return [];
        }
        return apiResponse.body;
      })
    );
  }

  public postDocTemplate(docInstance: DocTemplate): Observable<any> {
    return this.api.callPost<DocTemplate>(this.servicePrefix + '/', docInstance);
  }

  public putDocTemplate(docInstance: DocTemplate): Observable<any> {
    return this.api.callPut(this.servicePrefix + '/', docInstance);
  }

  public deleteDocTemplate(publicID: number) {
    return this.api.callDelete<number>(this.servicePrefix + '/' + publicID);
  }

  // Validation functions
  public checkDocTemplateExists(docName: string) {
    return this.api.callGet<T>(`${ this.servicePrefix }/name/${ docName }`);
  }

}

// Form Validators
export const checkDocTemplateExistsValidator = (docApiService: DocapiService<DocTemplate>, time: number = 500) => {
  return (control: FormControl) => {
    return timer(time).pipe(switchMap(() => {
      return docApiService.checkDocTemplateExists(control.value).pipe(
        map(() => {
          return { docTemplateExists: true };
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
