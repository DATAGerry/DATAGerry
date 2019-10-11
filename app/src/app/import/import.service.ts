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
import { ApiCallService, ApiService, httpFileOptions, resp } from '../services/api-call.service';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { HttpHeaders, HttpParams } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class ImportService implements ApiService {

  public servicePrefix: string = 'import';
  private objectPrefix: string = 'object';

  constructor(private api: ApiCallService) {
  }

  public postObjectParser(file: File, config: any): Observable<any> {
    const formData = new FormData();
    formData.append('file', file, file.name);
    formData.append('parser_config', JSON.stringify(config));
    return this.api.callPost<any>(`${ this.servicePrefix }/${ this.objectPrefix }/parse/`, formData, httpFileOptions).pipe(
      map((apiResponse) => {
        return apiResponse.body;
      })
    );
  }

  public getObjectParserDefaultConfig(fileType: string): Observable<any> {
    return this.api.callGet<any>(`${ this.servicePrefix }/${ this.objectPrefix }/parser/default/${ fileType }/`).pipe(
      map((apiResponse) => {
        if (apiResponse.status === 204) {
          return {};
        }
        return apiResponse.body;
      })
    );
  }

  public getObjectImporters(): Observable<string[]> {
    return this.api.callGet<string[]>(`${ this.servicePrefix }/${ this.objectPrefix }/importer/`).pipe(
      map((apiResponse) => {
        if (apiResponse.status === 204) {
          return [];
        }
        return apiResponse.body;
      })
    );
  }

}
