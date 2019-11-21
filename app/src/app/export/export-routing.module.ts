import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { ExportTypesComponent } from './export-types/export-types.component';
import { NavigationComponent } from '../layout/structure/navigation/navigation.component';
import { SidebarComponent } from '../layout/structure/sidebar/sidebar.component';
import { BreadcrumbComponent } from '../layout/structure/breadcrumb/breadcrumb.component';
import { FooterComponent } from '../layout/structure/footer/footer.component';
import { ExportComponent } from './export.component';
import { ExportObjectsComponent } from './export-objects/export-objects/export-objects.component';
import { LAYOUT_COMPONENT_ROUTES } from '../layout/layout.module';
import { PermissionGuard } from '../auth/guards/permission.guard';

const routes: Routes = [
  {
    path: '',
    pathMatch: 'full',
    canActivate: [PermissionGuard],
    data: {
      breadcrumb: 'Overview',
      right: 'base.export.*'
    },
    component: ExportComponent
  },
  {
    path: 'objects',
    canActivate: [PermissionGuard],
    data: {
      breadcrumb: 'Objects',
      right: 'base.export.type.*'
    },
    component: ExportObjectsComponent
  },
  {
    path: 'types',
    canActivate: [PermissionGuard],
    data: {
      breadcrumb: 'Types',
      right: 'base.export.type.*'
    },
    component: ExportTypesComponent
  }
].concat(LAYOUT_COMPONENT_ROUTES);

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class ExportRoutingModule {
}
