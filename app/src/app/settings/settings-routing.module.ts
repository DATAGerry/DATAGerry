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
import { SettingsComponent } from './settings.component';
import { PermissionGuard } from '../auth/guards/permission.guard';
import { LAYOUT_COMPONENT_ROUTES } from '../layout/layout.module';

const routes: Routes = [
  {
    path: '',
    pathMatch: 'full',
    canActivate: [PermissionGuard],
    data: {
      breadcrumb: 'Overview',
      right: 'base.system.view'
    },
    component: SettingsComponent
  },
  {
    path: 'auth',
    canActivateChild: [PermissionGuard],
    data: {
      breadcrumb: 'Authentication'
    },
    loadChildren: () => import('./auth-settings/auth-settings.module').then(m => m.AuthSettingsModule)
  },
  {
    path: 'system',
    canActivateChild: [PermissionGuard],
    data: {
      breadcrumb: 'System'
    },
    loadChildren: () => import('./system/system.module').then(m => m.SystemModule)
  },
  {
    path: 'logs',
    data: {
      breadcrumb: 'Logs'
    },
    loadChildren: () => import('./log-settings/log-settings.module').then(m => m.LogSettingsModule)
  },
  {
    path: 'exportdjob',
    data: {
      breadcrumb: 'Exportd Job'
    },
    loadChildren: () => import('./exportd-job-settings/exportd-job-settings.module').then(m => m.ExportdJobSettingsModule)
  },
  {
    path: 'docapi',
    data: {
      breadcrumb: 'DocAPI'
    },
    loadChildren: () => import('./docapi-settings/docapi-settings.module').then(m => m.DocapiSettingsModule)
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes), RouterModule.forChild(LAYOUT_COMPONENT_ROUTES)],
  exports: [RouterModule]
})
export class SettingsRoutingModule { }
