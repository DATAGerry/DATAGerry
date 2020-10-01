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

const routes: Routes = [
  {
    path: '',
    pathMatch: 'full',
    canActivate: [PermissionGuard],
    data: {
      breadcrumb: 'Overview'
    },
    component: FrameworkComponent
  },
  {
    path: 'object',
    canActivateChild: [PermissionGuard],
    data: {
      breadcrumb: 'Object',
      right: 'base.framework.object.view'
    },
    loadChildren: () => import('./object/object.module').then(m => m.ObjectModule),
  },
  {
    path: 'type',
    canActivateChild: [PermissionGuard],
    data: {
      breadcrumb: 'Type',
      right: 'base.framework.type.view'
    },
    loadChildren: () => import('./type/type.module').then(m => m.TypeModule),
  },
  {
    path: 'category',
    canActivateChild: [PermissionGuard],
    data: {
      breadcrumb: 'Category',
      right: 'base.framework.category.view'
    },
    loadChildren: () => import('./category/category.module').then(m => m.CategoryModule),
  },
  {
    path: 'collection',
    canActivateChild: [PermissionGuard],
    data: {
      breadcrumb: 'Collection',
      right: 'base.framework.collection.view'
    },
    loadChildren: () => import('./collection/collection.module').then(m => m.CollectionModule)
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class FrameworkRoutingModule { }
