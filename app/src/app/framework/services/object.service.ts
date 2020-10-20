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
import { ApiCallService, ApiService, httpObserveOptions, resp } from '../../services/api-call.service';
import { ValidatorService } from '../../services/validator.service';
import { CmdbObject } from '../models/cmdb-object';
import { Observable } from 'rxjs';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { map } from 'rxjs/operators';
import { RenderResult } from '../models/cmdb-render';
import { HttpClient, HttpHeaders, HttpResponse } from '@angular/common/http';
import { DataTableFilter, DataTablesResult } from '../models/cmdb-datatable';
import { GeneralModalComponent } from '../../layout/helpers/modals/general-modal/general-modal.component';
import { CmdbType } from '../models/cmdb-type';
import { APIGetSingleResponse } from '../../services/models/api-response';

export const httpObjectObserveOptions = {
  headers: new HttpHeaders({
    'Content-Type': 'application/json'
  }),
  observe: resp
};

export const PARAMETER = 'params';
export const FILTER = 'filter';
export const COOCKIENAME = 'onlyActiveObjCookie';

@Injectable({
  providedIn: 'root'
})

export class ObjectService<T = RenderResult> implements ApiService {

  public servicePrefix: string = 'object';

  constructor(private api: ApiCallService, private http: HttpClient, private modalService: NgbModal) {
  }

  // Find calls
  public getObjects(typeID: number, filter: DataTableFilter): Observable<T[]> {
    httpObjectObserveOptions[PARAMETER] = { onlyActiveObjCookie: this.api.readCookies(COOCKIENAME) };
    httpObjectObserveOptions[PARAMETER].start = filter.start;
    httpObjectObserveOptions[PARAMETER].length = filter.length;
    httpObjectObserveOptions[PARAMETER].order = filter.orderBy;
    httpObjectObserveOptions[PARAMETER].direction = filter.direction;
    httpObjectObserveOptions[FILTER] = filter;
    if (typeID != null) {
      return this.api.callGet<T[]>(`${ this.servicePrefix }/dt/type/${ typeID }`, httpObjectObserveOptions).pipe(
        map((apiResponse) => {
          if (apiResponse.status === 204) {
            return [];
          }
          return apiResponse.body;
        })
      );
    }

    return this.api.callGet<T[]>(`${ this.servicePrefix }/`, httpObjectObserveOptions).pipe(
      map((apiResponse) => {
        return apiResponse.body;
      })
    );
  }

  public getObjectsByType(typeID: number): Observable<T[]> {
    httpObjectObserveOptions[PARAMETER] = { onlyActiveObjCookie: this.api.readCookies(COOCKIENAME) };
    return this.api.callGet<T[]>(`${ this.servicePrefix }/type/${ typeID }`, httpObjectObserveOptions).pipe(
      map((apiResponse) => {
        if (apiResponse.status === 204) {
          return [];
        }
        return apiResponse.body;
      })
    );
  }

  public getObject<R>(publicID: number, native: boolean = false): Observable<R> {
    if (native === true) {
      return this.api.callGet<CmdbObject[]>(`${ this.servicePrefix }/${ publicID }/native/`).pipe(
        map((apiResponse) => {
          return apiResponse.body;
        })
      );
    }
    return this.api.callGet<R[]>(`${ this.servicePrefix }/${ publicID }/`).pipe(
      map((apiResponse) => {
        return apiResponse.body;
      })
    );
  }

  // CRUD calls
  public postObject(objectInstance: CmdbObject): Observable<any> {
    return this.api.callPost<CmdbObject>(this.servicePrefix + '/', objectInstance).pipe(
      map((apiResponse) => {
        return apiResponse.body;
      })
    );
  }

  public putObject(publicID: number, objectInstance: CmdbObject,
                   httpOptions = httpObserveOptions): Observable<any> {
    return this.api.callPut<CmdbObject>(`${ this.servicePrefix }/${ publicID }/`, objectInstance, httpOptions);
  }

  public changeState(publicID: number, status: boolean) {
    return this.api.callPut<boolean>(`${ this.servicePrefix }/${ publicID }/state/`, status).pipe(
      map((apiResponse) => {
        return apiResponse.body;
      })
    );
  }

  public deleteManyObjects(publicID: any) {
    return this.api.callDeleteManyRoute(`${ this.servicePrefix }/delete/${ publicID }`).pipe(
      map((apiResponse) => {
        if (apiResponse.status === 204) {
          return [];
        }
        return apiResponse.body;
      })
    );
  }

  public deleteObject(publicID: any): Observable<any> {
    return this.api.callDelete(`${ this.servicePrefix }/${ publicID }`);
  }

  // Count calls

  public countObjectsByType(typeID: number) {
    httpObjectObserveOptions[PARAMETER] = { onlyActiveObjCookie: this.api.readCookies(COOCKIENAME) };
    return this.api.callGet<number>(this.servicePrefix + '/count/' + typeID, httpObjectObserveOptions).pipe(
      map((apiResponse) => {
        if (apiResponse.status === 204) {
          return [];
        }
        return apiResponse.body;
      })
    );
  }

  public groupObjectsByType(value: string) {
    httpObjectObserveOptions[PARAMETER] = { onlyActiveObjCookie: this.api.readCookies(COOCKIENAME) };
    return this.api.callGet<any>(this.servicePrefix + '/group/' + value, httpObjectObserveOptions).pipe(
      map((apiResponse) => {
        if (apiResponse.status === 204) {
          return [];
        }
        return apiResponse.body;
      })
    );
  }

  public countObjects() {
    httpObjectObserveOptions[PARAMETER] = { onlyActiveObjCookie: this.api.readCookies(COOCKIENAME) };
    return this.api.callGet<number>(`${ this.servicePrefix }/count/`, httpObjectObserveOptions).pipe(
      map((apiResponse) => {
        if (apiResponse.status === 204) {
          return [];
        }
        return apiResponse.body;
      })
    );
  }

  // Custom calls
  public getObjectReferences(publicID: number) {
    httpObjectObserveOptions[PARAMETER] = { onlyActiveObjCookie: this.api.readCookies(COOCKIENAME) };
    return this.api.callGet<RenderResult[]>(`${ this.servicePrefix }/reference/${ publicID }`, httpObjectObserveOptions).pipe(
      map((apiResponse) => {
        if (apiResponse.status === 204) {
          return [];
        }
        return apiResponse.body;
      })
    );
  }

  public getObjectsByUser(publicID: number) {
    return this.api.callGet<RenderResult[]>(`${ this.servicePrefix }/user/${ publicID }`).pipe(
      map((apiResponse) => {
        if (apiResponse.status === 204) {
          return [];
        }
        return apiResponse.body;
      })
    );
  }

  public getNewObjectsSince(timestamp: number) {
    return this.api.callGet<RenderResult[]>(`${ this.servicePrefix }/user/new/${ timestamp }`).pipe(
      map((apiResponse) => {
        if (apiResponse.status === 204) {
          return [];
        }
        return apiResponse.body;
      })
    );
  }

  public getChangedObjectsSince(timestamp: number) {
    return this.api.callGet<RenderResult[]>(`${ this.servicePrefix }/user/changed/${ timestamp }`).pipe(
      map((apiResponse) => {
        if (apiResponse.status === 204) {
          return [];
        }
        return apiResponse.body;
      })
    );
  }

  public getObjectsByFilter(typeID: number, filter: DataTableFilter) {
    httpObjectObserveOptions[PARAMETER] = { onlyActiveObjCookie: this.api.readCookies(COOCKIENAME) };
    httpObjectObserveOptions[PARAMETER].start = filter.start;
    httpObjectObserveOptions[PARAMETER].length = filter.length;
    httpObjectObserveOptions[PARAMETER].order = filter.orderBy;
    httpObjectObserveOptions[PARAMETER].direction = filter.direction;
    httpObjectObserveOptions[PARAMETER].search = ValidatorService.validateRegex(filter.search).trim();
    httpObjectObserveOptions[PARAMETER].dtRender = filter.dtRender;
    httpObjectObserveOptions[PARAMETER].idList = filter.idList;
    return this.api.callGet<DataTablesResult[]>(`${ this.servicePrefix }/dt/filter/type/${ typeID }`,
      httpObjectObserveOptions).pipe(
      map((apiResponse) => {
        if (apiResponse.status === 204) {
          return [];
        }
        return apiResponse.body;
      })
    );
  }

  public async getUncleanObjects(typeID: number): Promise<boolean> {
    return this.api.callHead<CmdbType>(`${ this.servicePrefix }/clean/${ typeID }`).pipe(
      map((apiResponse) => {
        return +apiResponse.headers.get('X-Total-Count') > 0;
      })
    ).toPromise();
  }

  public cleanObjects(typeID: number): Observable<any> {
    return this.api.callPatch(`${ this.servicePrefix }/clean/${ typeID }`, null).pipe(
      map((apiResponse) => {
        return apiResponse.body;
      })
    );
  }

  public openModalComponent(title: string,
                            modalMessage: string,
                            buttonDeny: string,
                            buttonAccept: string) {

    const modalComponent = this.modalService.open(GeneralModalComponent);
    modalComponent.componentInstance.title = title;
    modalComponent.componentInstance.modalMessage = modalMessage;
    modalComponent.componentInstance.buttonDeny = buttonDeny;
    modalComponent.componentInstance.buttonAccept = buttonAccept;
    return modalComponent;
  }
}
