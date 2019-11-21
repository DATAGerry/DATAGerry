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

import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { AuthGuard } from './auth/guards/auth.guard';
import { HTTP_INTERCEPTORS } from '@angular/common/http';
import { HttpErrorInterceptor } from './error/interceptors/http-error.interceptor.tx';
import { PermissionGuard } from './auth/guards/permission.guard';

const routes: Routes = [
  {
    path: 'connect',
    loadChildren: () => import('./connect/connect.module').then(m => m.ConnectModule)
  },
  {
    path: 'auth',
    loadChildren: () => import('./auth/auth.module').then(m => m.AuthModule)
  },
  {
    path: '',
    canActivate: [AuthGuard],
    data: {
      breadcrumb: 'Dashboard'
    },
    loadChildren: () => import('./dashboard/dashboard.module').then(m => m.DashboardModule)
  },
  {
    path: 'search',
    canActivate: [AuthGuard, PermissionGuard],
    data: {
      breadcrumb: 'Search',
      right: 'base.framework.*'
    },
    loadChildren: () => import('./search/search.module').then(m => m.SearchModule)
  },
  {
    path: 'framework',
    canActivate: [AuthGuard],
    canActivateChild: [PermissionGuard],
    data: {
      breadcrumb: 'Framework'
    },
    loadChildren: () => import('./framework/framework.module').then(m => m.FrameworkModule)
  },
  {
    path: 'import',
    canActivate: [AuthGuard],
    data: {
      breadcrumb: 'Import',
      right: 'base.import.*'
    },
    loadChildren: () => import('./import/import.module').then(m => m.ImportModule)
  },
  {
    path: 'export',
    canActivate: [AuthGuard, PermissionGuard],
    data: {
      breadcrumb: 'Export',
      right: 'base.export.*'
    },
    loadChildren: () => import('./export/export.module').then(m => m.ExportModule)
  },
  {
    path: 'management',
    canActivate: [AuthGuard, PermissionGuard],
    data: {
      breadcrumb: 'User-Management',
      right: 'base.user-management.*'
    },
    loadChildren: () => import('./management/management.module').then(m => m.ManagementModule),
  },
  {
    path: 'settings',
    canActivate: [AuthGuard, PermissionGuard],
    data: {
      breadcrumb: 'Settings',
      right: 'base.system.*'
    },
    loadChildren: () => import('./settings/settings.module').then(m => m.SettingsModule)
  },
  {
    path: 'error',
    loadChildren: () => import('./error/error.module').then(m => m.ErrorModule)
  },
  {
    path: '**',
    redirectTo: 'error/404'
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {
}
