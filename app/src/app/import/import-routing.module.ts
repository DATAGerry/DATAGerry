/*
* DATAGERRY - OpenSource Enterprise CMDB
* Copyright (C) 2024 becon GmbH
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
import { ImportComponent } from './import.component';
import { ImportObjectsComponent } from './import-objects/import-objects.component';
import { ImportTypesComponent } from './import-types/import-types.component';
import { PermissionGuard } from '../auth/guards/permission.guard';

const routes: Routes = [
  {
    path: '',
    pathMatch: 'full',
    canActivate: [PermissionGuard],
    data: {
      breadcrumb: 'Overview'
    },
    component: ImportComponent
  },
  {
    path: 'object',
    canActivate: [PermissionGuard],
    data: {
      breadcrumb: 'Object',
      right: 'base.import.object.*'
    },
    component: ImportObjectsComponent
  },
  {
    path: 'type',
    canActivate: [PermissionGuard],
    data: {
      breadcrumb: 'Type',
      right: 'base.import.type.*'
    },
    component: ImportTypesComponent
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class ImportRoutingModule {
}
