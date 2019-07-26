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
import { HttpClient } from '@angular/common/http';
import { ConnectionService } from './connection.service';
import { map } from 'rxjs/operators';
import { DatePipe } from '@angular/common';
import { FileSaverService } from 'ngx-filesaver';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ExportService {

  private readonly apiPrefix = 'rest';
  private readonly apiURL;

  constructor(private http: HttpClient, private connectionService: ConnectionService, private datePipe: DatePipe,
              private fileSaverService: FileSaverService) {
    this.apiURL = `${this.connectionService.connectionURL}${this.apiPrefix}/`;
  }

  public callFileFormatRoute<T>(route: string, params?: any): Observable<any> {
    return this.http.get<T>(this.apiURL + route, params);
  }

  public callExportRoute<T>(route: string, fileExtension: string) {
    const REQUEST_URI = this.apiURL + route;

    return this.http.get(REQUEST_URI, {
      observe: 'response',
      responseType: 'blob'
    }).pipe(
      map(res => {
        const timestamp = this.datePipe.transform(new Date(), 'MM_dd_yyyy_hh_mm_ss');
        return {
          filename: timestamp + '.' + fileExtension,
          data: res
        };
      })
    ).subscribe(res => {
      this.fileSaverService.save(res.data.body, res.filename);
    }, error => {
      console.log('download error:', JSON.stringify(error));
    }, () => {
      console.log('Completed file download.');
    });
  }
}
