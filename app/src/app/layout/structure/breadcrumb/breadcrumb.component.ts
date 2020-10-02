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

import { Component, Input, OnInit, ViewEncapsulation } from '@angular/core';
import { filter } from 'rxjs/operators';
import { BreadcrumbItem } from './breadcrumb.model';
import { BreadcrumbService } from './breadcrumb.service';
import { ActivatedRoute, NavigationEnd, PRIMARY_OUTLET, Router } from '@angular/router';

export const COOCKIENAME = 'onlyActiveObjCookie';

@Component({
  selector: 'cmdb-breadcrumb',
  templateUrl: './breadcrumb.component.html',
  styleUrls: ['./breadcrumb.component.scss'],
  encapsulation: ViewEncapsulation.None
})
export class BreadcrumbComponent implements OnInit {

  @Input()
  public allowBootstrap: boolean = true;

  @Input()
  public addClass: string;

  public isChecked: boolean;

  public constructor(public breadcrumbService: BreadcrumbService, private activatedRoute: ActivatedRoute, private router: Router) {

  }

  public hasParams(breadcrumb: BreadcrumbItem) {
    return Object.keys(breadcrumb.params).length ? [breadcrumb.url, breadcrumb.params] : [breadcrumb.url];
  }


  public ngOnInit() {
    if (this.router.navigated) {
      this.breadcrumbService.store(this.getBreadcrumbs(this.activatedRoute.root));
    }

    this.router.events.pipe(
      filter(event => event instanceof NavigationEnd
      )).subscribe(() => {
      this.breadcrumbService.store(this.getBreadcrumbs(this.activatedRoute.root));
    });
    this.isChecked = this.readCookies(COOCKIENAME) === 'true';
  }

  private getBreadcrumbs(route: ActivatedRoute, url: string= '', breadcrumbs: BreadcrumbItem[]= []): BreadcrumbItem[] {
    const ROUTE_DATA_BREADCRUMB: string = 'breadcrumb';
    const currentRoute: ActivatedRoute[] = route.children;

    if (currentRoute.length === 0) {
      return breadcrumbs;
    }

    for (const child of currentRoute) {
      if (child.outlet !== PRIMARY_OUTLET) {
        continue;
      }

      if (!child.snapshot.data.hasOwnProperty(ROUTE_DATA_BREADCRUMB)) {
        return this.getBreadcrumbs(child, url, breadcrumbs);
      }

      const routeURL: string = child.snapshot.url.map(segment => segment.path).join('/');
      url += `/${routeURL}`;

      const breadcrumb: BreadcrumbItem = {
        label: child.snapshot.data[ROUTE_DATA_BREADCRUMB],
        params: child.snapshot.params,
        queryParams: child.snapshot.queryParams,
        url
      };
      breadcrumbs.push(breadcrumb);

      return this.getBreadcrumbs(child, url, breadcrumbs);
    }
  }

  public checkState(event: any) {
    this.writeCookies(COOCKIENAME, event.currentTarget.checked.toString());
    window.location.reload();
  }

  readCookies(name: string) {
    const result = new RegExp('(?:^|; )' + encodeURIComponent(name) + '=([^;]*)').exec(document.cookie);
    return result ? result[1] : 'true';
  }

  writeCookies(name: string, value: string, days?: number) {
    if (!days) {
      days = 365 * 20;
    }

    const date = new Date();
    date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));

    const expires = '; expires=' + date.toUTCString();
    document.cookie = name + '=' + value + expires + '; path=/';
  }
}
