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
import { CmdbType } from '../models/cmdb-type';
import { ApiCallService } from '../../services/api-call.service';

@Injectable({
  providedIn: 'root'
})
export class TypeService {

  private servicePrefix: string = 'type';
  private typeList: CmdbType[];

  constructor(private api: ApiCallService) {
    this.getTypeList().subscribe((respTypeList: CmdbType[]) => {
      this.typeList = respTypeList;
    });
  }

  public findType(publicID: number): CmdbType {
    return this.typeList.find(id => id.public_id === publicID);
  }

  public getType(publicID: number) {
    return this.api.callGetRoute<CmdbType>(this.servicePrefix + '/' + publicID);
  }

  public getTypeList() {
    return this.api.callGetRoute<CmdbType[]>(this.servicePrefix + '/');
  }

  public async validateTypeName(name: string) {
    return this.typeList.find(type => type.name === name) === undefined;
  }

  public postType(typeInstance: CmdbType) {
    return this.api.callPostRoute<number>(this.servicePrefix + '/', typeInstance);
  }

  public putType(typeInstance: CmdbType) {
    return this.api.callPutRoute(this.servicePrefix + '/', typeInstance);
  }

  public deleteType(publicID: number) {
    return this.api.callDeleteRoute<number>(this.servicePrefix + '/' + publicID);
  }

}

