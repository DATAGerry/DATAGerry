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
import { LAYOUT_COMPONENT_ROUTES } from '../layout/layout.module';
import { PermissionGuard } from '../auth/guards/permission.guard';

const routes: Routes = [
  {
    path: 'users',
    canActivateChild: [PermissionGuard],
    data: {
      breadcrumb: 'Users',
    },
    loadChildren: () => import('./users/users.module').then(m => m.UsersModule)
  },
  {
    path: 'groups',
    canActivateChild: [PermissionGuard],
    data: {
      breadcrumb: 'Groups',
      right: 'base.user-management.group.*'
    },
    loadChildren: () => import('./groups/groups.module').then(m => m.GroupsModule)
  },
  {
    path: 'rights',
    canActivateChild: [PermissionGuard],
    data: {
      breadcrumb: 'Rights',
    },
    loadChildren: () => import('./rights/rights.module').then(m => m.RightsModule)
  }
].concat(LAYOUT_COMPONENT_ROUTES);


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class ManagementRoutingModule {
}
