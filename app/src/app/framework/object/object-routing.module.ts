/*
* dataGerry - OpenSource Enterprise CMDB
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
import { ObjectListComponent } from './components/object-list/object-list.component';
import { ObjectViewComponent } from './object-view/object-view.component';
import { ObjectAddComponent } from './object-add/object-add.component';

const routes: Routes = [
  {
    path: '',
    data: {
      breadcrumb: 'List'
    },
    component: ObjectListComponent
  },
  {
    path: 'add',
    data: {
      breadcrumb: 'New'
    },
    component: ObjectAddComponent
  },
  {
    path: 'type/:publicID',
    data: {
      breadcrumb: 'List / Type'
    },
    component: ObjectListComponent
  },
  {
    path: ':publicID',
    component: ObjectViewComponent
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class ObjectRoutingModule { }
