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
import { UsersListComponent } from './users-list/users-list.component';
import { UsersAddComponent } from './users-add/users-add.component';
import { UserViewComponent } from './user-view/user-view.component';
import { UsersEditComponent } from './users-edit/users-edit.component';
import { UsersDeleteComponent } from './users-delete/users-delete.component';

const routes: Routes = [
  {
    path: '',
    data: {
      breadcrumb: 'List',
      right: 'base.user-management.user.view'
    },
    component: UsersListComponent
  },
  {
    path: 'view/:publicID',
    data: {
      breadcrumb: 'View',
      right: 'base.user-management.user.view'
    },
    component: UserViewComponent
  },
  {
    path: 'add',
    data: {
      breadcrumb: 'Add',
      right: 'base.user-management.user.add'
    },
    component: UsersAddComponent
  },
  {
    path: 'edit/:publicID',
    data: {
      breadcrumb: 'Edit',
      right: 'base.user-management.user.edit'
    },
    component: UsersEditComponent
  },
  {
    path: 'delete/:publicID',
    data: {
      breadcrumb: 'Delete',
      right: 'base.user-management.user.delete'
    },
    component: UsersDeleteComponent
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class UsersRoutingModule {
}
