import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { ImportComponent } from './import.component';
import { NavigationComponent } from '../layout/components/navigation/navigation.component';
import { SidebarComponent } from '../layout/components/sidebar/sidebar.component';
import { BreadcrumbComponent } from '../layout/components/breadcrumb/breadcrumb.component';
import { ImportObjectsComponent } from './import-objects/import-objects.component';
import { FooterComponent } from '../layout/components/footer/footer.component';
import { ImportTypesComponent } from './import-types/import-types.component';

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
    component: ImportComponent
  },
  {
    path: 'object',
    data: {
      breadcrumb: 'Object'
    },
    component: ImportObjectsComponent
  },
  {
    path: 'type',
    data: {
      breadcrumb: 'Type'
    },
    component: ImportTypesComponent
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class ImportRoutingModule {
}
