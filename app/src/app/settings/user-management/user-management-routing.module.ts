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
import { GroupsListComponent } from './groups-list/groups-list.component';
import { RightsListComponent } from './rights-list/rights-list.component';

const routes: Routes = [
  {
    path: '',
    data: {
      breadcrumb: 'List'
    },
    component: UsersListComponent
  },
  {
    path: 'groups',
    data: {
      breadcrumb: 'List'
    },
    component: GroupsListComponent
  },
  {
    path: 'rights',
    data: {
      breadcrumb: 'List'
    },
    component: RightsListComponent
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class UserManagementRoutingModule { }
