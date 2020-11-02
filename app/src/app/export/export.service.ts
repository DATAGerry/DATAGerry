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
import { ApiCallService, httpFileOptions} from '../services/api-call.service';
import { map } from 'rxjs/operators';
import { HttpParams } from '@angular/common/http';

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

  public callExportRoute(objectIDs: string, exportType: string, zipping: boolean = false) {
    const options = httpFileOptions;
    let params = new HttpParams();
    params = params.set('ids', objectIDs);
    params = params.set('classname', exportType);
    params = params.set('zip', JSON.stringify(zipping));
    options.params = params;

    return this.api.callGet<any>(this.servicePrefix + '/object/', httpFileOptions);
  }

  public getObjectFileByType(typeID: number, exportType: string) {
    return this.api.callGet(this.servicePrefix + '/object/type/' + typeID + '/' + exportType, httpFileOptions);
  }

  public getTypeFile() {
    return this.api.callPost<any>('export/type/', null, httpFileOptions);
  }

  public callExportTypeRoute(route: string) {
    return this.api.callPost<any>(route , null, httpFileOptions);
  }
}
