/*
* DATAGERRY - OpenSource Enterprise CMDB
* Copyright (C) 2019 - 2021 NETHINKS GmbH
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
* along with this program. If not, see <https://www.gnu.org/licenses/>.
*/

import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { ExportdJobSettingsListComponent } from './exportd-job-settings-list/exportd-job-settings-list.component';
import { ExportdJobSettingsAddComponent } from './exportd-job-settings-add/exportd-job-settings-add.component';
import { ExportdJobSettingsEditComponent } from './exportd-job-settings-edit/exportd-job-settings-edit.component';
import { ExportdJobSettingsCopyComponent } from './exportd-job-settings-copy/exportd-job-settings-copy.component';
import { ExportdJobLogsComponent } from './exportd-job-logs/exportd-job-logs.component';
import { PermissionGuard } from '../auth/guards/permission.guard';
import { UserSettingsResolver } from '../management/user-settings/resolvers/user-settings-resolver.service';

const routes: Routes = [
  {
    path: '',
    data: {
      breadcrumb: 'List',
    },
    canActivate: [PermissionGuard],
    resolve: {
      userSetting: UserSettingsResolver
    },
    component: ExportdJobSettingsListComponent
  },
  {
    path: 'add',
    data: {
      breadcrumb: 'Add'
    },
    canActivate: [PermissionGuard],
    component: ExportdJobSettingsAddComponent
  },
  {
    path: 'edit/:publicID',
    data: {
      breadcrumb: 'Edit'
    },
    canActivate: [PermissionGuard],
    component: ExportdJobSettingsEditComponent
  },
  {
    path: 'copy/:publicID',
    data: {
      breadcrumb: 'Copy'
    },
    canActivate: [PermissionGuard],
    component: ExportdJobSettingsCopyComponent
  },
  {
    path: 'log/:publicID',
    data: {
      breadcrumb: 'Log'
    },
    canActivate: [PermissionGuard],
    component: ExportdJobLogsComponent
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class ExportdRoutingModule { }
