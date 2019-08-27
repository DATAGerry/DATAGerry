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
import { BreadcrumbItem } from './breadcrumb.model';
import { Observable, Subject } from 'rxjs';

@Injectable()
export class BreadcrumbService {

  private breadcrumbs: BreadcrumbItem[];
  private readonly prefixedBreadcrumbs: BreadcrumbItem[] = [];
  public breadcrumbsSource: Subject<BreadcrumbItem[]>;
  public breadcrumbsChanged$: Observable<BreadcrumbItem[]>;

  constructor() {
    this.breadcrumbs = [];
    this.breadcrumbsSource = new Subject<BreadcrumbItem[]>();
    this.breadcrumbsChanged$ = this.breadcrumbsSource.asObservable();

    if (localStorage.getItem('prefixedBreadcrumbs') != null) {
      this.prefixedBreadcrumbs = (JSON.parse(localStorage.getItem('prefixedBreadcrumbs')));
    }
  }

  public store(breadcrumbs: BreadcrumbItem[]) {
    this.breadcrumbs = breadcrumbs;

    const allBreadcrumbs = this.prefixedBreadcrumbs.concat(this.breadcrumbs);
    this.breadcrumbsSource.next(allBreadcrumbs);

  }

  public storePrefixed(breadcrumb: BreadcrumbItem) {
    this.storeIfUnique(breadcrumb);
    localStorage.setItem('prefixedBreadcrumbs', JSON.stringify(this.prefixedBreadcrumbs));
    const allBreadcrumbs = this.prefixedBreadcrumbs.concat(this.breadcrumbs);
    this.breadcrumbsSource.next(allBreadcrumbs);

  }

  public get() {
    return this.breadcrumbsChanged$;
  }

  private storeIfUnique(newBreadcrumb: BreadcrumbItem) {
    let isUnique = true;
    for (const crumb of this.prefixedBreadcrumbs) {
      if (newBreadcrumb.url === crumb.url) {
        isUnique = false;
        break;
      }
    }
    if (isUnique) {
      this.prefixedBreadcrumbs.push(newBreadcrumb);
    }

  }

}
