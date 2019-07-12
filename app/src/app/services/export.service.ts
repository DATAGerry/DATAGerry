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

@Injectable({
  providedIn: 'root'
})
export class ExportService {

  private readonly apiPrefix = 'rest';
  private readonly apiURL;

  constructor(private http: HttpClient, private connectionService: ConnectionService) {
    this.apiURL = `${this.connectionService.connectionURL}${this.apiPrefix}/`;
  }

  public callExportRoute<T>(route: string, httpHeader) {
    const REQUEST_HEADERS = httpHeader;
    const REQUEST_URI = this.apiURL + route;

    return this.http.get(REQUEST_URI,  {
      headers: REQUEST_HEADERS,
      responseType: 'text'
    });
  }
}
