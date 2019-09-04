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
import { ObjectListComponent } from './object-list/object-list.component';
import { ObjectViewComponent } from './object-view/object-view.component';
import { ObjectAddComponent } from './object-add/object-add.component';
import { ObjectEditComponent } from './object-edit/object-edit.component';
import { ObjectCopyComponent } from './object-copy/object-copy.component';
import { ObjectLogComponent } from './object-log/object-log.component';

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
    path: 'add/:publicID',
    data: {
      breadcrumb: 'Add'
    },
    component: ObjectAddComponent
  },
  {
    path: 'edit/:publicID',
    data: {
      breadcrumb: 'Edit'
    },
    component: ObjectEditComponent
  },
  {
    path: 'copy/:publicID',
    data: {
      breadcrumb: 'Copy'
    },
    component: ObjectCopyComponent
  },
  {
    path: 'type/:publicID',
    data: {
      breadcrumb: 'List'
    },
    component: ObjectListComponent
  },
  {
    path: 'view/:publicID',
    data: {
      breadcrumb: 'View'
    },
    component: ObjectViewComponent
  },
  {
    path: 'log/:publicID',
    data: {
      breadcrumb: 'View Log'
    },
    component: ObjectLogComponent
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class ObjectRoutingModule {
}
