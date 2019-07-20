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
import { CommonModule } from '@angular/common';

import { UserManagementRoutingModule } from './user-management-routing.module';
import { RightsListComponent } from './rights-list/rights-list.component';
import { GroupsListComponent } from './groups-list/groups-list.component';
import { UsersListComponent } from './users-list/users-list.component';
import { MasterBadgeComponent } from './rights-list/master-badge/master-badge.component';
import { LevelHighlightComponent } from './rights-list/level-highlight/level-highlight.component';

@NgModule({
  declarations: [RightsListComponent, GroupsListComponent, UsersListComponent, MasterBadgeComponent, LevelHighlightComponent],
  imports: [
    CommonModule,
    UserManagementRoutingModule
  ]
})
export class UserManagementModule { }
