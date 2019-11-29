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
import { NavigationStart, Router } from '@angular/router';
import { BackendHttpError } from '../models/custom.error';
import { Observable, Subject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ErrorMessageService {

  private keepAfterRouteChange = false;
  private error: Subject<BackendHttpError> = new Subject<BackendHttpError>();

  public constructor(private router: Router) {
    /*this.router.events.subscribe(event => {
      if (event instanceof NavigationStart) {
        if (this.keepAfterRouteChange) {
          this.keepAfterRouteChange = false;
        } else {
          this.clear();
        }
      }
    });*/
  }

  public getError(): Observable<any> {
    return this.error.asObservable();
  }

  public add(error: BackendHttpError) {
    this.error.next(error);
  }

  public remove(error: BackendHttpError) {
    this.error.next(error);
  }

  private clear(): void {
    this.error.next();
  }

}
