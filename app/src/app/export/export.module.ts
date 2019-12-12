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
    FontAwesomeModule
  ]
})
export class ExportModule { }
