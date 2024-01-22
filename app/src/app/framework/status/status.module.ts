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
import { CommonModule } from '@angular/common';

import { StatusRoutingModule } from './status-routing.module';
import { StatusComponent } from './status.component';
import { StatusListComponent } from './status-list/status-list.component';
import { StatusAddComponent } from './status-add/status-add.component';
import { StatusEditComponent } from './status-edit/status-edit.component';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { LayoutModule } from '../../layout/layout.module';

@NgModule({
  declarations: [StatusComponent, StatusListComponent, StatusAddComponent, StatusEditComponent],
  imports: [
    CommonModule,
    StatusRoutingModule,
    LayoutModule,
    ReactiveFormsModule
  ]
})
export class StatusModule { }
