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

import { DashboardRoutingModule } from './dashboard-routing.module';
import { DashboardComponent } from './dashboard.component';
import { LayoutModule } from '../layout/layout.module';
import { DashcardComponent } from './components/dashcard/dashcard.component';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { RenderModule } from '../framework/render/render.module';
import { UsersModule } from '../management/users/users.module';
import { ObjectModule } from '../framework/object/object.module';
import { TableModule } from '../layout/table/table.module';

@NgModule({
  declarations: [DashboardComponent, DashcardComponent],
  imports: [
    CommonModule,
    LayoutModule,
    DashboardRoutingModule,
    FontAwesomeModule,
    RenderModule,
    UsersModule,
    ObjectModule,
    TableModule
  ]
})
export class DashboardModule {
}
