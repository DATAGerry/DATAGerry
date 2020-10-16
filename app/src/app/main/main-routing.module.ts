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
import { DashboardComponent } from '../dashboard/dashboard.component';


const routes: Routes = [
  {
    path: '',
    data: {
      breadcrumb: 'Dashboard'
    },
    component: DashboardComponent
    // loadChildren: () => import('../dashboard/dashboard.module').then(m => m.DashboardModule)
  },
  {
    path: 'error',
    data: {
      breadcrumb: 'Error'
    },
    loadChildren: () => import('../error/error.module').then(m => m.ErrorModule)
  },
  {
    path: 'search',
    data: {
      breadcrumb: 'Search'
    },
    loadChildren: () => import('../search/search.module').then(m => m.SearchModule)
  },
  {
    path: 'framework',
    data: {
      breadcrumb: 'Framework'
    },
    loadChildren: () => import('../framework/framework.module').then(m => m.FrameworkModule)
  },
  {
    path: 'import',
    data: {
      breadcrumb: 'Import'
    },
    loadChildren: () => import('../import/import.module').then(m => m.ImportModule)
  },
  {
    path: 'export',
    data: {
      breadcrumb: 'Export'
    },
    loadChildren: () => import('../export/export.module').then(m => m.ExportModule)
  },
  {
    path: 'management',
    data: {
      breadcrumb: 'User-Management'
    },
    loadChildren: () => import('../management/management.module').then(m => m.ManagementModule),
  },
  {
    path: 'settings',
    data: {
      breadcrumb: 'Settings'
    },
    loadChildren: () => import('../settings/settings.module').then(m => m.SettingsModule)
  },
  {
    path: 'info',
    data: {
      breadcrumb: 'Info'
    },
    loadChildren: () => import('../info/info.module').then(m => m.InfoModule)
  },
  {
    path: 'filemanager',
    data: {
      breadcrumb: 'Filemanager'
    },
    loadChildren: () => import('../filemanager/filemanager.module').then(m => m.FilemanagerModule)
  },
  {
    path: 'debug',
    data: {
      breadcrumb: 'Debug'
    },
    loadChildren: () => import('../debug/debug.module').then(m => m.DebugModule)
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class MainRoutingModule {
}
