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
