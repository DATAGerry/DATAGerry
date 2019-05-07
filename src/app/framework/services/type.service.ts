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
import { Observable } from 'rxjs';
import { CmdbType } from '../models/cmdb-type';
import { ApiCallService } from '../../services/api-call.service';

@Injectable({
  providedIn: 'root'
})
export class TypeService {

  private servicePrefix: string = 'type';
  public typeObservable;

  constructor(private api: ApiCallService) {
    this.typeObservable = Observable.create((observer: any) => {
      this.api.callGetRoute<CmdbType[]>(this.servicePrefix + '/').subscribe(
        list => {
          for (const typeInstance of list) {
            observer.next(typeInstance);
          }
        }, (error: any) => {
          console.log(error);
        },
        () => {
          observer.complete();
        });
    });
  }


  public getTypeList() {
    return this.api.callGetRoute<CmdbType[]>(this.servicePrefix + '/');
  }
}
