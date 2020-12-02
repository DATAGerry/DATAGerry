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


import { Inject, Injectable, Optional } from '@angular/core';
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

import { InjectionToken, Type } from '@angular/core';
import { ProgressBarService } from '../layout/progress/progress-bar.service';

interface ProgressRouterConfig {
  id?: string;
  delay?: number;
  startEvents?: Type<RouterEvent>[];
  completeEvents?: Type<RouterEvent>[];
}

export const PROGRESS_ROUTER_CONFIG = new InjectionToken<ProgressRouterConfig>('progressRouterConfig');

@Injectable({
  providedIn: 'root'
})
export class AppLoadingService {

  private readonly config: ProgressRouterConfig = {
    id: 'app',
    delay: 0,
    startEvents: [NavigationStart],
    completeEvents: [NavigationEnd, NavigationCancel, NavigationError]
  };

  constructor(private router: Router, progressService: ProgressBarService,
              @Optional() @Inject(PROGRESS_ROUTER_CONFIG) config: ProgressRouterConfig) {
    this.config = config ? { ...this.config, ...config } : this.config;
    console.log(this.config);
  }

  public isNavigationPending: Observable<boolean> = this.router.events.pipe(
    filter((event: RouterEvent) => AppLoadingService.isConsideredEvent(event)),
    map((event: RouterEvent) => AppLoadingService.isNavigationStart(event)),
    distinctUntilChanged()
  );

  private static isConsideredEvent(event: RouterEvent): boolean {
    return AppLoadingService.isNavigationStart(event)
      || AppLoadingService.isNavigationEnd(event);
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
