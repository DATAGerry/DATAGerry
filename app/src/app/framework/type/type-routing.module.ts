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
import { TypeListComponent } from './type-list/type-list.component';
import { TypeAddComponent } from './type-add/type-add.component';
import { TypeEditComponent } from './type-edit/type-edit.component';
import { TypeDeleteComponent } from './type-delete/type-delete.component';

const routes: Routes = [
  {
    path: '',
    data: {
      breadcrumb: 'List'
    },
    component: TypeListComponent
  },
  {
    path: 'add',
    data: {
      breadcrumb: 'Add'
    },
    component: TypeAddComponent
  },
  {
    path: 'edit/:publicID',
    data: {
      breadcrumb: 'Edit'
    },
    component: TypeEditComponent
  },
  {
    path: 'delete/:publicID',
    data: {
      breadcrumb: 'Delete'
    },
    component: TypeDeleteComponent
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class TypeRoutingModule { }
