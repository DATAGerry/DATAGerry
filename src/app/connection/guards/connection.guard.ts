/*
* Net|CMDB - OpenSource Enterprise CMDB
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
import { CanActivate, ActivatedRouteSnapshot, RouterStateSnapshot, UrlTree, Router } from '@angular/router';
import { Observable } from 'rxjs';
import { ConnectionService } from '../services/connection.service';
import { connectableObservableDescriptor } from 'rxjs/internal/observable/ConnectableObservable';

@Injectable({
  providedIn: 'root'
})
export class ConnectionGuard implements CanActivate {

  private connectionIntervalTime: number = 10;
  private interval: any;

  constructor(private router: Router, private connectionService: ConnectionService) {
    // check if connection exists
    this.interval = setInterval(() => {
      if (!this.connectionService.isConnected) {
        this.router.navigate(['/connection']);
      }
    }, this.connectionIntervalTime * 1000);
  }

  canActivate(
    next: ActivatedRouteSnapshot,
    state: RouterStateSnapshot): Observable<boolean | UrlTree> | Promise<boolean | UrlTree> | boolean | UrlTree {
    const currentConnection = this.connectionService.currentConnection;
    if (currentConnection) {
      return true;
    }
    this.router.navigate(['/connection'], {queryParams: {returnUrl: state.url}});
    return false;
  }

}
