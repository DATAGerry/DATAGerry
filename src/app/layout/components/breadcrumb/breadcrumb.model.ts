import { Params } from '@angular/router';

export interface BreadcrumbItem {
  label: string;
  params: Params;
  url: string;
}
