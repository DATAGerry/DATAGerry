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
* along with this program. If not, see <https://www.gnu.org/licenses/>.
*/

import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AclObjectsInformationTableComponent } from './components/acl-objects-information-table/acl-objects-information-table.component';
import { TableModule } from '../layout/table/table.module';
import { LayoutModule } from '../layout/layout.module';
import { AclObjectsInformationActivationColumnComponent } from './components/acl-objects-information-activation-column/acl-objects-information-activation-column.component';
import { AclObjectsInformationPermissionsColumnComponent } from './components/acl-objects-information-permissions-column/acl-objects-information-permissions-column.component';
import { ReactiveFormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';

@NgModule({
  declarations: [AclObjectsInformationTableComponent, AclObjectsInformationActivationColumnComponent, AclObjectsInformationPermissionsColumnComponent],
  exports: [
    AclObjectsInformationTableComponent
  ],
  imports: [
    CommonModule,
    TableModule,
    LayoutModule,
    ReactiveFormsModule,
    RouterModule
  ]
})
export class AclModule {
}
