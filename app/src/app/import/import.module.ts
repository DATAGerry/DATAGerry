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

import { ImportRoutingModule } from './import-routing.module';
import { ImportComponent } from './import.component';
import { LayoutModule } from '../layout/layout.module';
import { ImportObjectsComponent } from './import-objects/import-objects.component';
import { ArchwizardModule } from 'angular-archwizard';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import { NgSelectModule } from '@ng-select/ng-select';
import { FileConfigComponent } from './import-objects/file-config/file-config.component';
import { CsvConfigComponent } from './import-objects/file-config/csv-config/csv-config.component';
import { JsonConfigComponent } from './import-objects/file-config/json-config/json-config.component';
import { ImportTypesComponent } from './import-types/import-types.component';
import { TypeModule } from '../framework/type/type.module';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { DndModule } from 'ngx-drag-drop';
import { RenderModule } from '../framework/render/render.module';
import { NgbTooltipModule } from '@ng-bootstrap/ng-bootstrap';
import { SelectFileComponent } from './import-objects/select-file/select-file.component';
import { ImportConfigComponent } from './import-objects/import-config/import-config.component';
import { TypeMappingComponent } from './import-objects/type-mapping/type-mapping.component';
import { JsonMappingComponent } from './import-objects/type-mapping/json-mapping/json-mapping.component';
import { TypeMappingBaseComponent } from './import-objects/type-mapping/type-mapping-base.component';
import { CsvMappingComponent } from './import-objects/type-mapping/csv-mapping/csv-mapping.component';
import { MappingControlPipe } from './import-objects/type-mapping/mapping-control.pipe';
import { SelectFileDragDropComponent } from './import-types/select-file-drag-drop/select-file-drag-drop.component';
import { TypePreviewComponent } from './import-types/type-preview/type-preview.component';
import { CategoryModule } from '../framework/category/category.module';
import { ImportTypeCompleteComponent } from './import-types/import-type-complete/import-type-complete.component';
import { ImportCompleteComponent } from './import-objects/import-complete/import-complete.component';
import { DataTablesModule } from 'angular-datatables';
import {TableModule} from "../layout/table/table.module";
import { FailedImportTableComponent } from './import-objects/import-complete/failed-import-table/failed-import-table.component';


@NgModule({
  entryComponents: [JsonConfigComponent, CsvConfigComponent, JsonMappingComponent, CsvMappingComponent],
  declarations: [
    ImportComponent,
    ImportObjectsComponent,
    SelectFileComponent,
    FileConfigComponent,
    CsvConfigComponent,
    JsonConfigComponent,
    ImportTypesComponent,
    ImportConfigComponent,
    TypeMappingComponent,
    JsonMappingComponent,
    TypeMappingBaseComponent,
    CsvMappingComponent,
    MappingControlPipe,
    SelectFileDragDropComponent,
    TypePreviewComponent,
    ImportTypeCompleteComponent,
    ImportCompleteComponent,
    FailedImportTableComponent,
  ],
  imports: [
    CommonModule,
    LayoutModule,
    ImportRoutingModule,
    DndModule,
    ArchwizardModule,
    ReactiveFormsModule,
    NgSelectModule,
    TypeModule,
    FontAwesomeModule,
    RenderModule,
    NgbTooltipModule,
    FormsModule,
    CategoryModule,
    TableModule
  ]
})
export class ImportModule {
}
