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

import { NgModule, isDevMode } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { AuthGuard } from './auth/guards/auth.guard';

const routes: Routes = [
  {
    path: '',
    pathMatch: 'full',
    canActivateChild: [AuthGuard],
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
    path: 'error',
    canActivate: [AuthGuard],
    data: {
      breadcrumb: 'Error'
    },
    loadChildren: () => import('./error/error.module').then(m => m.ErrorModule)
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
    path: 'framework',
    canActivate: [AuthGuard],
    data: {
      breadcrumb: 'Framework'
    },
    loadChildren: () => import('./framework/framework.module').then(m => m.FrameworkModule)
  },
  {
    path: 'import',
    canActivate: [AuthGuard],
    data: {
      breadcrumb: 'Import'
    },
    loadChildren: () => import('./import/import.module').then(m => m.ImportModule)
  },
  {
    path: 'export',
    canActivate: [AuthGuard],
    data: {
      breadcrumb: 'Export'
    },
    loadChildren: () => import('./export/export.module').then(m => m.ExportModule)
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
    path: 'info',
    canActivate: [AuthGuard],
    data: {
      breadcrumb: 'Info'
    },
    loadChildren: () => import('./info/info.module').then(m => m.InfoModule)
  },
  {
    path: 'filemanager',
    canActivate: [AuthGuard],
    data: {
      breadcrumb: 'Filemanager'
    },
    loadChildren: () => import('./file-manager/file-manager.module').then(m => m.FileManagerModule)
  },
  {
    path: 'debug',
    canActivate: [AuthGuard],
    data: {
      breadcrumb: 'Debug'
    },
    loadChildren: () => import('./debug/debug.module').then(m => m.DebugModule)
  },
  {
    path: '**',
    redirectTo: '/error/404'
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {
}
