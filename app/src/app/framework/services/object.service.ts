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
import { ApiCallService, ApiService } from '../../services/api-call.service';
import { CmdbObject } from '../models/cmdb-object';
import { Observable } from 'rxjs';
import { ModalComponent } from '../../layout/helpers/modal/modal.component';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { map } from 'rxjs/operators';
import { RenderResult } from '../models/cmdb-render';
import { HttpBackend, HttpClient } from '@angular/common/http';
import { AuthService } from '../../auth/services/auth.service';

@Injectable({
  providedIn: 'root'
})
export class ObjectService<T = RenderResult> implements ApiService {

  public servicePrefix: string = 'object';

  constructor(private api: ApiCallService, private modalService: NgbModal) {
  }

  // Find calls
  public getObjectsByType(typeID: number): Observable<T[]> {
    return this.api.callGet<T[]>(`${this.servicePrefix}/type/${typeID}`).pipe(
      map((apiResponse) => {
        if (apiResponse.status === 204) {
          return [];
        }
        return apiResponse.body;
      })
    );
  }

  public getObject<R>(publicID: number, native: boolean = false, specialClient?: HttpClient): Observable<R> {
    if (native === true) {
      return this.api.callGet<CmdbObject[]>(`${this.servicePrefix}/${publicID}/native/`).pipe(
        map((apiResponse) => {
          return apiResponse.body;
        })
      );
    }
    return this.api.callGet<R[]>(`${this.servicePrefix}/${publicID}/`, specialClient).pipe(
      map((apiResponse) => {
        return apiResponse.body;
      })
    );
  }

  // CRUD calls
  public postObject(objectInstance: CmdbObject): Observable<any> {
    return this.api.callPostRoute<CmdbObject>(this.servicePrefix + '/', objectInstance);
  }

  public putObject(publicID: number, objectInstance: CmdbObject): Observable<any> {
    return this.api.callPutRoute<CmdbObject>(`${this.servicePrefix}/${publicID}/`, objectInstance);
  }

  public changeState(publicID: number, status: boolean) {
    return this.api.callPut<boolean>(`${this.servicePrefix}/${publicID}/state/`, status).pipe(
      map((apiResponse) => {
        return apiResponse.body;
      })
    );
  }

  // Count calls

  public countObjectsByType(typeID: number) {
    return this.api.callGetRoute<number>(this.servicePrefix + '/count/' + typeID);
  }

  public countObjects() {
    return this.api.callGet<number>(`${this.servicePrefix}/count/`).pipe(
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
    return this.api.callGet<RenderResult[]>(`${this.servicePrefix}/reference/${publicID}`).pipe(
      map((apiResponse) => {
        if (apiResponse.status === 204) {
          return [];
        }
        return apiResponse.body;
      })
    );
  }

  public getObjectsByUser(publicID: number) {
    return this.api.callGet<RenderResult[]>(`${this.servicePrefix}/user/${publicID}`).pipe(
      map((apiResponse) => {
        if (apiResponse.status === 204) {
          return [];
        }
        return apiResponse.body;
      })
    );
  }

  public getNewObjectsSince(timestamp: number) {
    return this.api.callGet<RenderResult[]>(`${this.servicePrefix}/user/new/${timestamp}`).pipe(
      map((apiResponse) => {
        if (apiResponse.status === 204) {
          return [];
        }
        return apiResponse.body;
      })
    );
  }

  public getChangedObjectsSince(timestamp: number) {
    return this.api.callGet<RenderResult[]>(`${this.servicePrefix}/user/changed/${timestamp}`).pipe(
      map((apiResponse) => {
        if (apiResponse.status === 204) {
          return [];
        }
        return apiResponse.body;
      })
    );
  }


  public openModalComponent(title: string,
                            modalMessage: string,
                            buttonDeny: string,
                            buttonAccept: string) {

    const modalComponent = this.modalService.open(ModalComponent);
    modalComponent.componentInstance.title = title;
    modalComponent.componentInstance.modalMessage = modalMessage;
    modalComponent.componentInstance.buttonDeny = buttonDeny;
    modalComponent.componentInstance.buttonAccept = buttonAccept;
    return modalComponent;
  }
}
