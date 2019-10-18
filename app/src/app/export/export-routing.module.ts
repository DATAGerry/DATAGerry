import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { ExportTypesComponent } from './export-types/export-types.component';
import { NavigationComponent } from '../layout/components/navigation/navigation.component';
import { SidebarComponent } from '../layout/components/sidebar/sidebar.component';
import { BreadcrumbComponent } from '../layout/components/breadcrumb/breadcrumb.component';
import { FooterComponent } from '../layout/components/footer/footer.component';
import { ExportComponent } from './export.component';
import {ExportObjectsComponent} from "./export-objects/export-objects/export-objects.component";

const routes: Routes = [
  {
    path: '',
    component: NavigationComponent,
    outlet: 'navigation'
  },
  {
    path: '',
    component: SidebarComponent,
    outlet: 'sidebar'
  },
  {
    path: '',
    component: BreadcrumbComponent,
    outlet: 'breadcrumb'
  },
  {
    path: '',
    component: FooterComponent,
    outlet: 'footer'
  },
  {
    path: '',
    data: {
      breadcrumb: 'Overview'
    },
    component: ExportComponent
  },
  {
    path: 'types',
    data: {
      breadcrumb: 'Types'
    },
    component: ExportTypesComponent
  },
  {
    path: 'objects',
    data: {
      breadcrumb: 'Objects'
    },
    component: ExportObjectsComponent
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class ExportRoutingModule { }
