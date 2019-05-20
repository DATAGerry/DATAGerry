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
import { debounceTime, map } from 'rxjs/operators';
import { ApiCallService } from './api-call.service';
import { Subject } from "rxjs";

@Injectable()
export class ShareDataService {

  private dataResult = new Subject<any>();

  constructor(private api: ApiCallService) {

  }


  getDataResult() {
    return this.dataResult.asObservable();
  }

  setDataResult(newValue) {
    this.dataResult.next(newValue)
  }

  public searchTerm(route: string) {
    const result = this.api.callGetRoute(route, {params: {limit: '5'}})
      .pipe(
        debounceTime(500),  // WAIT FOR 500 MILISECONDS ATER EACH KEY STROKE.
        map(
          (data: any) => {
            return (
              data.length > 0 ? data as any[] : [{'Object': 'No Object Found'} as any]
            );
          }
        ));

    return result;
  }
}
