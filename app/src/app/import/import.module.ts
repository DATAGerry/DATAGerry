import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { ImportRoutingModule } from './import-routing.module';
import { ImportComponent } from './import.component';
import { LayoutModule } from '../layout/layout.module';
import { SweetAlert2Module } from '@sweetalert2/ngx-sweetalert2';
import { ImportObjectsComponent } from './import-objects/import-objects.component';
import { ArchwizardModule } from 'angular-archwizard';
import { ReactiveFormsModule } from '@angular/forms';
import { SelectTypeComponent } from './import-objects/select-type/select-type.component';
import { SelectFileComponent } from './import-objects/select-file/select-file.component';
import { NgSelectModule } from '@ng-select/ng-select';
import { PreviewComponent } from './import-objects/preview/preview.component';
import { FileConfigComponent } from './import-objects/file-config/file-config.component';
import { CsvConfigComponent } from './import-objects/file-config/csv-config/csv-config.component';
import { JsonConfigComponent } from './import-objects/file-config/json-config/json-config.component';
import { CsvPreviewComponent } from './import-objects/preview/csv-preview/csv-preview.component';
import { ImportTypesComponent } from './import-types/import-types.component';
import { TypeModule } from '../framework/type/type.module';

@NgModule({
  entryComponents: [JsonConfigComponent, CsvConfigComponent, CsvPreviewComponent],
  declarations: [ImportComponent, ImportObjectsComponent, SelectTypeComponent, SelectFileComponent, PreviewComponent,
    FileConfigComponent, CsvConfigComponent, JsonConfigComponent, CsvPreviewComponent, ImportTypesComponent],
  imports: [
    CommonModule,
    LayoutModule,
    ImportRoutingModule,
    SweetAlert2Module,
    ArchwizardModule,
    ReactiveFormsModule,
    NgSelectModule,
    TypeModule
  ]
})
export class ImportModule {
}
