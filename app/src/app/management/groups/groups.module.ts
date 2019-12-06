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
import { CommonModule } from '@angular/common';

import { GroupsRoutingModule } from './groups-routing.module';
import { GroupsListComponent } from './groups-list/groups-list.component';
import { DataTablesModule } from 'angular-datatables';
import { GroupsAddComponent } from './groups-add/groups-add.component';
import { ReactiveFormsModule } from '@angular/forms';
import { NgSelectModule } from '@ng-select/ng-select';
import { GroupsEditComponent } from './groups-edit/groups-edit.component';
import { GroupsDeleteComponent } from './groups-delete/groups-delete.component';
import { LayoutModule } from '../../layout/layout.module';
import { GroupSelectPipe } from './groups-delete/group-select.pipe';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import {AuthModule} from "../../auth/auth.module";

@NgModule({
  declarations: [GroupsListComponent, GroupsAddComponent, GroupsEditComponent, GroupsDeleteComponent, GroupSelectPipe],
    imports: [
        CommonModule,
        GroupsRoutingModule,
        DataTablesModule,
        ReactiveFormsModule,
        NgSelectModule,
        LayoutModule,
        FontAwesomeModule,
        AuthModule
    ]
})
export class GroupsModule {
}
