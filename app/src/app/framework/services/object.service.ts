/*
* dataGerry - OpenSource Enterprise CMDB
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
import {Observable} from "rxjs";

@Injectable({
  providedIn: 'root'
})
export class ObjectService {

  private servicePrefix: string = 'object';
  public objectList: CmdbObject[];

  constructor(private api: ApiCallService) {
    this.getObjectList().subscribe((resObjectList: CmdbObject[]) => {
      this.objectList = resObjectList;
    });
  }

  public countObjectsByType(typeID: number) {
    return this.api.callGetRoute<number>(this.servicePrefix + '/count/' + typeID);
  }

  public getObjectList() {
    return this.api.callGetRoute<CmdbObject[]>(this.servicePrefix + '/');
  }

  public getObjectsByType(typeID: number) {
    return this.api.callGetRoute<CmdbObject[]>(this.servicePrefix + '/type/' + typeID);
  }

  public postAddObject(objectInstance: CmdbObject): Observable<any>{
    return this.api.callPostRoute<CmdbObject>(this.servicePrefix + '/add', objectInstance);
  }

  public postUpdateObject(objectInstance: CmdbObject): Observable<any>{
    return this.api.callPutRoute<CmdbObject>(this.servicePrefix + '/', objectInstance);
  }
}
