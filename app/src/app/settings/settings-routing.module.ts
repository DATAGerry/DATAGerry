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
import { NavigationComponent } from '../layout/structure/navigation/navigation.component';
import { SidebarComponent } from '../layout/structure/sidebar/sidebar.component';
import { BreadcrumbComponent } from '../layout/structure/breadcrumb/breadcrumb.component';
import { FooterComponent } from '../layout/structure/footer/footer.component';
import { SettingsComponent } from './settings.component';
import { LAYOUT_COMPONENT_ROUTES } from '../layout/layout.module';
import { PermissionGuard } from '../auth/guards/permission.guard';

const routes: Routes = [
  {
    path: '',
    pathMatch: 'full',
    canActivate: [PermissionGuard],
    data: {
      breadcrumb: 'Overview',
      right: 'base.system.*'
    },
    component: SettingsComponent
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
    loadChildren: () => import('./task-settings/task-settings.module').then(m => m.TaskSettingsModule)
  }
].concat(LAYOUT_COMPONENT_ROUTES);

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class SettingsRoutingModule { }
