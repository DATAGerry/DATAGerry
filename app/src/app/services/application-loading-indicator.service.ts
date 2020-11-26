/*
* DATAGERRY - OpenSource Enterprise CMDB
* Copyright (C) 2019 - 2020 NETHINKS GmbH
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
* along with this program. If not, see <https://www.gnu.org/licenses/>.
*/

import { Injectable } from '@angular/core';
import {
  NavigationCancel,
  NavigationEnd,
  NavigationError,
  NavigationStart,
  Router,
  RouterEvent
} from '@angular/router';
import { Observable } from 'rxjs';
import { distinctUntilChanged, filter, map } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class ApplicationLoadingIndicatorService {

  constructor(private router: Router) {
  }

  public isNavigationPending: Observable<boolean> = this.router.events.pipe(
    filter((event: RouterEvent) => ApplicationLoadingIndicatorService.isConsideredEvent(event)),
    map((event: RouterEvent) => ApplicationLoadingIndicatorService.isNavigationStart(event)),
    distinctUntilChanged()
  );

  private static isConsideredEvent(event: RouterEvent): boolean {
    return ApplicationLoadingIndicatorService.isNavigationStart(event)
      || ApplicationLoadingIndicatorService.isNavigationEnd(event);
  }

  private static isNavigationStart(event: RouterEvent): boolean {
    return event instanceof NavigationStart;
  }

  private static isNavigationEnd(event: RouterEvent): boolean {
    return event instanceof NavigationEnd
      || event instanceof NavigationCancel
      || event instanceof NavigationError;
  }
}
