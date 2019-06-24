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

import { ObjectRoutingModule } from './object-routing.module';
import { ObjectListComponent } from './components/object-list/object-list.component';
import { ObjectViewComponent } from './components/object-view/object-view.component';
import { DataTablesModule } from 'angular-datatables';
import { LayoutModule } from '../../layout/layout.module';
import { ObjectHeaderComponent } from './components/object-header/object-header.component';
import { ObjectQrComponent } from './components/object-qr/object-qr.component';
import { QRCodeModule } from 'angularx-qrcode';
import { ObjectSummaryComponent } from './components/object-summary/object-summary.component';
import { ObjectExternalsComponent } from './components/object-externals/object-externals.component';
import { ObjectFieldsViewComponent } from './components/object-fields-view/object-fields-view.component';
import { NgxSpinnerModule } from 'ngx-spinner';
import { ObjectInsertComponent } from './components/object-insert/object-insert.component';
import {FormsModule, ReactiveFormsModule} from "@angular/forms";

@NgModule({
  declarations: [ObjectListComponent, ObjectViewComponent, ObjectHeaderComponent, ObjectQrComponent, ObjectSummaryComponent,
    ObjectExternalsComponent, ObjectFieldsViewComponent, ObjectInsertComponent],
  imports: [
    CommonModule,
    ObjectRoutingModule,
    DataTablesModule,
    LayoutModule,
    QRCodeModule,
    NgxSpinnerModule,
    FormsModule,
    ReactiveFormsModule
  ]
})
export class ObjectModule { }
