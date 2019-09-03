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
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { CmdbLog } from '../models/cmdb-log';

@Injectable({
  providedIn: 'root'
})
export class LogService<T = CmdbLog> implements ApiService  {

  public servicePrefix: string = 'log';

  constructor(private api: ApiCallService) {
  }

  public getLogsByObject(publicID: number) {
    return this.api.callGet<T>(`${this.servicePrefix}/object/${publicID}/`).pipe(
      map((apiResponse) => {
        return apiResponse.body;
      })
    );
  }

}
