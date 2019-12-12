import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { ExportTypesComponent } from './export-types/export-types.component';
import { ExportComponent } from './export.component';
import { ExportObjectsComponent } from './export-objects/export-objects.component';
import { PermissionGuard } from '../auth/guards/permission.guard';
import { LAYOUT_COMPONENT_ROUTES } from '../layout/layout.module';

const routes: Routes = [
  {
    path: '',
    pathMatch: 'full',
    canActivate: [PermissionGuard],
    data: {
      breadcrumb: 'Overview'
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
];

@NgModule({
  imports: [RouterModule.forChild(routes), RouterModule.forChild(LAYOUT_COMPONENT_ROUTES)],
  exports: [RouterModule]
})
export class ExportRoutingModule {
}
