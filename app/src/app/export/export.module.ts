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
import { ExportRoutingModule } from './export-routing.module';
import { ExportComponent } from './export.component';
import { ExportTypesComponent } from './export-types/export-types.component';
import { LayoutModule } from '../layout/layout.module';
import { ArchwizardModule } from 'angular-archwizard';
import { ReactiveFormsModule } from '@angular/forms';
import { ExportObjectsComponent } from './export-objects/export-objects.component';
import { NgSelectModule } from '@ng-select/ng-select';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { AuthModule } from '../auth/auth.module';

@NgModule({
  declarations: [
    ExportComponent,
    ExportTypesComponent,
    ExportObjectsComponent],
    imports: [
        CommonModule,
        LayoutModule,
        ExportRoutingModule,
        ArchwizardModule,
        ReactiveFormsModule,
        NgSelectModule,
        FontAwesomeModule,
        AuthModule
    ]
})
export class ExportModule { }
