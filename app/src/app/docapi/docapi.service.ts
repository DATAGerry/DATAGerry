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

import { HttpInterceptorHandler, ApiCallService, ApiService } from '../services/api-call.service';
import { HttpBackend, HttpClient, HttpResponse } from '@angular/common/http';
import { FormControl } from '@angular/forms';
import { switchMap, map, catchError } from 'rxjs/operators';
import { Observable, timer } from 'rxjs';
import { AuthService } from '../auth/services/auth.service';
import { DocTemplate } from '../framework/models/cmdb-doctemplate';
import { BasicAuthInterceptor } from '../auth/interceptors/basic-auth.interceptor';

const fileHttpOptions = {
  observe: 'response',
  responseType: 'blob'
};


@Injectable({
  providedIn: 'root'
})
export class DocapiService<T = DocTemplate> implements ApiService {

  public readonly servicePrefix: string = 'docapi/template';

  constructor(private api: ApiCallService, private backend: HttpBackend, private authService: AuthService) {
  }

  getDocTemplateList() : Observable<T[]> {
    return this.api.callGet<T>(`${ this.servicePrefix }/`).pipe(
      map((apiResponse) => {
        if (apiResponse.status === 204) {
          return [];
        }
        return apiResponse.body;
      })
    );
  }


  getObjectDocTemplateList(typeId: number) : Observable<T[]> {
    const searchfilter = {
        template_type: 'OBJECT',
        template_parameters: { type: typeId }
    }
    return this.api.callGet<T>(`${ this.servicePrefix }/by/${JSON.stringify(searchfilter)}`).pipe(
      map((apiResponse) => {
        if (apiResponse.status === 204) {
          return [];
        }
        return apiResponse.body;
      })
    );
  }


  getRenderedObjectDoc(templateId: number, objectId: number) {
    return this.api.callGetRoute<any>(`${ this.servicePrefix }/${ templateId }/render/${ objectId }`, fileHttpOptions);
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
    return this.api.callPostRoute<DocTemplate>(this.servicePrefix + '/', docInstance);
  }

  public putDocTemplate(docInstance: DocTemplate): Observable<any> {
    return this.api.callPutRoute(this.servicePrefix + '/', docInstance);
  }

  public deleteDocTemplate(publicID: number) {
    return this.api.callDeleteRoute<number>(this.servicePrefix + '/' + publicID);
  }

  // Validation functions
  public checkDocTemplateExists(docName: string) {
    const specialClient = new HttpClient(new HttpInterceptorHandler(this.backend, new BasicAuthInterceptor()));
    return this.api.callGet<T>(`${ this.servicePrefix }/${ docName }`, specialClient);
  }

}

//Form Validators
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
