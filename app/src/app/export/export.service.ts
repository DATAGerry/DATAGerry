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
import { ApiCallService } from '../services/api-call.service';
import {map} from "rxjs/operators";

const httpOptions = {
  observe: 'response',
  responseType: 'blob'
};

@Injectable({
  providedIn: 'root'
})
export class FileService {

  private servicePrefix: string = 'file';

  constructor(private api: ApiCallService) {
  }

  public callFileFormatRoute() {
    return this.api.callGet<any>(this.servicePrefix + '/').pipe(
      map((apiResponse) => {
        return apiResponse.body;
      })
    );
  }

  public callExportRoute(route: string, exportType: string) {
    return this.api.callPostRoute<any>(route + '/' + exportType,
      null, httpOptions);
  }

  public getObjectFileByType(typeID: number, exportType: string) {
    return this.api.callPostRoute(this.servicePrefix + '/object/type/' + typeID + '/' + exportType,
      null, httpOptions);
  }

  public getTypeFile() {
    return this.api.callPostRoute<any>('export/type/', null, httpOptions);
  }

  public callExportTypeRoute(route: string) {
    return this.api.callPostRoute<any>(route , null, httpOptions);
  }
}
