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

import { Component, Input, OnInit, ViewEncapsulation } from '@angular/core';
import { filter } from 'rxjs/operators';
import { BreadcrumbItem } from './breadcrumb.model';
import { BreadcrumbService } from './breadcrumb.service';
import { ActivatedRoute, NavigationEnd, PRIMARY_OUTLET, Router } from '@angular/router';


@Component({
  selector: 'cmdb-breadcrumb',
  templateUrl: './breadcrumb.component.html',
  styleUrls: ['./breadcrumb.component.scss'],
  encapsulation: ViewEncapsulation.None
})
export class BreadcrumbComponent implements OnInit {
  private ROUTE_DATA_BREADCRUMB: string = 'breadcrumb';
  private ROUTE_PARAM_BREADCRUMB: string = 'breadcrumb';
  private PREFIX_BREADCRUMB: string = 'prefixBreadcrumb';

  private currentBreadcrumbs: BreadcrumbItem[];
  public breadcrumbs: BreadcrumbItem[];

  @Input()
  public allowBootstrap: boolean = true;

  @Input()
  public addClass: string;


  public constructor(private breadcrumbService: BreadcrumbService, private activatedRoute: ActivatedRoute, private router: Router) {
    breadcrumbService.get().subscribe((breadcrumbs: BreadcrumbItem[]) => {
      this.breadcrumbs = breadcrumbs as BreadcrumbItem[];
    });
  }

  public hasParams(breadcrumb: BreadcrumbItem) {
    return Object.keys(breadcrumb.params).length ? [breadcrumb.url, breadcrumb.params] : [breadcrumb.url];
  }


  public ngOnInit() {
    if (this.router.navigated) {
      this.generateBreadcrumbTrail();
    }

    this.router.events.pipe(
      filter(event => event instanceof NavigationEnd
      )).subscribe(event => {
      this.generateBreadcrumbTrail();
    });
  }

  private generateBreadcrumbTrail() {
    this.currentBreadcrumbs = [];

    let currentRoute: ActivatedRoute = this.activatedRoute.root;

    let url: string = '';

    while (currentRoute.children.length > 0) {
      const childrenRoutes: ActivatedRoute[] = currentRoute.children;
      let breadCrumbLabel: string = '';

      childrenRoutes.forEach(route => {
        currentRoute = route;
        if (route.outlet !== PRIMARY_OUTLET) {
          return;
        }
        const hasData = (route.routeConfig && route.routeConfig.data);
        const hasDynamicBreadcrumb: boolean = route.snapshot.params.hasOwnProperty(this.ROUTE_PARAM_BREADCRUMB);

        if (hasData || hasDynamicBreadcrumb) {
          if (hasDynamicBreadcrumb) {
            breadCrumbLabel = route.snapshot.params[this.ROUTE_PARAM_BREADCRUMB].replace(/_/g, ' ');
          } else if (route.snapshot.data.hasOwnProperty(this.ROUTE_DATA_BREADCRUMB)) {
            breadCrumbLabel = route.snapshot.data[this.ROUTE_DATA_BREADCRUMB];
          }
          const routeURL: string = route.snapshot.url.map(segment => segment.path).join('/');
          url += `/${routeURL}`;
          if (routeURL.length === 0) {
            route.snapshot.params = {};
          }
          const breadcrumb: BreadcrumbItem = {
            label: breadCrumbLabel,
            params: route.snapshot.params,
            url: url
          };
          if (route.snapshot.data.hasOwnProperty(this.PREFIX_BREADCRUMB)) {
            this.breadcrumbService.storePrefixed(breadcrumb);
          } else {
            this.currentBreadcrumbs.push(breadcrumb);
          }
        }
      });
      this.breadcrumbService.store(this.currentBreadcrumbs);
    }
  }
}
