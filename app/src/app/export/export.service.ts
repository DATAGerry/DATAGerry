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
import { ApiCallService, httpFileOptions } from '../services/api-call.service';
import { map } from 'rxjs/operators';
import { HttpParams } from '@angular/common/http';
import { CollectionParameters } from '../services/models/api-parameter';

@Injectable({
  providedIn: 'root'
})
export class FileService {

  private servicePrefix: string = 'exporter';

  constructor(private api: ApiCallService) {
  }

  public callFileFormatRoute() {
    return this.api.callGet<any>(this.servicePrefix + '/extensions').pipe(
      map((apiResponse) => {
        return apiResponse.body;
      })
    );
  }

  public callExportRoute(params: CollectionParameters) {
    const options = httpFileOptions;
    let httpParams: HttpParams = new HttpParams();
    if (params.filter !== undefined) {
      httpParams = httpParams.set('filter', JSON.stringify(params.filter));
    }
    if (params.optional !== undefined) {
      for (const key of Object.keys(params.optional)) {
        httpParams = httpParams.set(key, params.optional[key]);
      }
    }
    options.params = httpParams;
    return this.api.callGet<any>(this.servicePrefix + '/', options);
  }

  public getTypeFile() {
    return this.api.callPost<any>('export/type/', null, httpFileOptions);
  }

  public callExportTypeRoute(route: string) {
    return this.api.callPost<any>(route , null, httpFileOptions);
  }
}
