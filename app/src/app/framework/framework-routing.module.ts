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
import { FrameworkComponent } from './framework.component';
import { PermissionGuard } from '../auth/guards/permission.guard';
import { LAYOUT_COMPONENT_ROUTES } from '../layout/layout.module';

const routes: Routes = [
  {
    path: '',
    pathMatch: 'full',
    canActivate: [PermissionGuard],
    data: {
      breadcrumb: 'Overview',
      right: 'base.framework.*'
    },
    component: FrameworkComponent
  },
  {
    path: 'object',
    canActivateChild: [PermissionGuard],
    data: {
      breadcrumb: 'Object'
    },
    loadChildren: () => import('./object/object.module').then(m => m.ObjectModule),
  },
  {
    path: 'type',
    canActivateChild: [PermissionGuard],
    data: {
      breadcrumb: 'Type'
    },
    loadChildren: () => import('./type/type.module').then(m => m.TypeModule),
  },

  {
    path: 'category',
    canActivateChild: [PermissionGuard],
    data: {
      breadcrumb: 'Category'
    },
    loadChildren: () => import('./category/category.module').then(m => m.CategoryModule),
  }
].concat(LAYOUT_COMPONENT_ROUTES);

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class FrameworkRoutingModule { }
