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

const routes: Routes = [
  {
    path: '',
    canActivate: [AuthGuard],
    data: {
      breadcrumb: 'Dashboard'
    },
    loadChildren: () => import('./dashboard/dashboard.module').then(m => m.DashboardModule)
  },
  {
    path: 'connect',
    loadChildren: () => import('./connect/connect.module').then(m => m.ConnectModule)
  },
  {
    path: 'auth',
    loadChildren: () => import('./auth/auth.module').then(m => m.AuthModule)
  },
  {
    path: 'search',
    canActivate: [AuthGuard],
    data: {
      breadcrumb: 'Search'
    },
    loadChildren: () => import('./search/search.module').then(m => m.SearchModule)
  },
  {
    path: 'file',
    canActivate: [AuthGuard],
    data: {
      breadcrumb: 'File'
    },
    loadChildren: () => import('./export/export.module').then(m => m.ExportModule)
  },
  {
    path: 'framework',
    canActivate: [AuthGuard],
    data: {
      breadcrumb: 'Framework'
    },
    loadChildren: () => import('./framework/framework.module').then(m => m.FrameworkModule)
  },
  {
    path: 'management',
    canActivate: [AuthGuard],
    data: {
      breadcrumb: 'User-Management'
    },
    loadChildren: () => import('./management/management.module').then(m => m.ManagementModule),
  },
  {
    path: 'settings',
    canActivate: [AuthGuard],
    data: {
      breadcrumb: 'Settings'
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
  exports: [RouterModule],
  providers: [
    {provide: HTTP_INTERCEPTORS, useClass: HttpErrorInterceptor, multi: true},
  ]
})
export class AppRoutingModule {
}
