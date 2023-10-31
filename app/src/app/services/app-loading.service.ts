/*
* DATAGERRY - OpenSource Enterprise CMDB
* Copyright (C) 2023 becon GmbH
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
import { Observable, of } from 'rxjs';
import { delay, distinctUntilChanged, filter, map, switchMap, tap } from 'rxjs/operators';

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
    delay: 100,
    startEvents: [NavigationStart],
    completeEvents: [NavigationEnd, NavigationCancel, NavigationError]
  };

  constructor(private router: Router, progressService: ProgressBarService,
              @Optional() @Inject(PROGRESS_ROUTER_CONFIG) config: ProgressRouterConfig) {
    this.config = config ? { ...this.config, ...config } : this.config;
    const progressBarInstance = progressService.getInstance(this.config.id);
    const startProgress = of({}).pipe(
      delay(this.config.delay),
      tap(() => progressBarInstance.start())
    );

    const completeProgress = of({}).pipe(
      delay(this.config.delay),
      tap(() => progressBarInstance.complete())
    );

    const filterEvents = [...this.config.startEvents, ...this.config.completeEvents];
    this.router.events.pipe(
      filter((event: RouterEvent) => AppLoadingService.eventExists(event, filterEvents)),
      switchMap((event: RouterEvent) => AppLoadingService.eventExists(event, this.config.startEvents) ? startProgress : completeProgress)
    ).subscribe();
  }

  /**
   * Function which shows if the router is pending.
   */
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

  static eventExists(routerEvent: RouterEvent, events: Type<RouterEvent>[]) {
    let res = false;
    events.map((event: Type<RouterEvent>) => res = res || routerEvent instanceof event);
    return res;
  }

}
