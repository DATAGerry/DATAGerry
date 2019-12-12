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
import { GroupsListComponent } from './groups-list/groups-list.component';
import { GroupsAddComponent } from './groups-add/groups-add.component';
import { GroupsEditComponent } from './groups-edit/groups-edit.component';
import { GroupsDeleteComponent } from './groups-delete/groups-delete.component';

const routes: Routes = [
  {
    path: '',
    pathMatch: 'full',
    data: {
      breadcrumb: 'List',
      right: 'base.user-management.group.view'
    },
    component: GroupsListComponent
  },
  {
    path: 'add',
    data: {
      breadcrumb: 'Add',
      right: 'base.user-management.group.add'
    },
    component: GroupsAddComponent
  },
  {
    path: 'edit/:publicID',
    data: {
      breadcrumb: 'Edit',
      right: 'base.user-management.group.edit'
    },
    component: GroupsEditComponent
  },
  {
    path: 'delete/:publicID',
    data: {
      breadcrumb: 'Delete',
      right: 'base.user-management.group.delete'
    },
    component: GroupsDeleteComponent
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class GroupsRoutingModule {
}
