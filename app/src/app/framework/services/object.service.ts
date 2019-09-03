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
import { ApiCallService } from '../../services/api-call.service';
import { CmdbObject } from '../models/cmdb-object';
import { Observable } from 'rxjs';
import { ModalComponent } from '../../layout/helpers/modal/modal.component';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { CmdbStatus } from '../models/cmdb-status';
import { map } from 'rxjs/operators';
import { RenderResult } from '../models/cmdb-render';

@Injectable({
  providedIn: 'root'
})
export class ObjectService {

  private servicePrefix: string = 'object';
  public objectList: CmdbObject[];

  constructor(private api: ApiCallService, private modalService: NgbModal) {
    this.getObjectList().subscribe((resObjectList: CmdbObject[]) => {
      this.objectList = resObjectList;
    });
  }

  // Find calls

  public getObjectList() {
    return this.api.callGetRoute<CmdbObject[]>(this.servicePrefix + '/');
  }

  public getObjectsByType(typeID: number) {
    return this.api.callGetRoute<CmdbObject[]>(this.servicePrefix + '/type/' + typeID);
  }

  public getObject(publicID: number, native: boolean = false) {
    if (native) {
      return this.api.callGetRoute<CmdbObject[]>(this.servicePrefix + '/' + publicID + '/native/');
    }
    return this.api.callGetRoute<CmdbObject[]>(this.servicePrefix + '/' + publicID);
  }

  // CRUD calls

  public postObject(objectInstance: CmdbObject): Observable<any> {
    return this.api.callPostRoute<CmdbObject>(this.servicePrefix + '/', objectInstance);
  }

  public putObject(publicID: number, objectInstance: CmdbObject): Observable<any> {
    return this.api.callPutRoute<CmdbObject>(`${this.servicePrefix}/${publicID}/`, objectInstance);
  }

  // Count calls

  public countObjectsByType(typeID: number) {
    return this.api.callGetRoute<number>(this.servicePrefix + '/count/' + typeID);
  }

  // Custom calls

  public getObjectReferences(publicID: number) {
    return this.api.callGet<RenderResult[]>(`${this.servicePrefix}/reference/${publicID}`).pipe(
      map((apiResponse) => {
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
