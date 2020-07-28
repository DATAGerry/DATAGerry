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
import { ExportdJobSettingsListComponent } from './exportd-job-settings-list/exportd-job-settings-list.component';
import { ExportdJobSettingsEditComponent } from './exportd-job-settings-edit/exportd-job-settings-edit.component';
import { ExportdJobSettingsAddComponent } from './exportd-job-settings-add/exportd-job-settings-add.component';
import { DataTablesModule } from 'angular-datatables';
import { ExportdJobSettingsRoutingModule } from './exportd-job-settings-routing.module';
import { LayoutModule } from '../../layout/layout.module';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import {
  ExportdJobSettingsBuilderComponent
} from './exportd-job-settings-builder/exportd-job-settings-builder.component';
import { ArchwizardModule } from 'angular-archwizard';
import {
  ExportdJobBasicStepComponent
} from './exportd-job-settings-builder/exportd-job-basic-step/exportd-job-basic-step.component';
import {
  ExportdJobSourcesStepComponent
} from './exportd-job-settings-builder/exportd-job-sources-step/exportd-job-sources-step.component';
import {
  ExportdJobDestinationsStepComponent
} from './exportd-job-settings-builder/exportd-job-destinations-step/exportd-job-destinations-step.component';
import {
  ExportdJobVariablesStepComponent,
  FilterPipe
} from './exportd-job-settings-builder/exportd-job-variables-step/exportd-job-variables-step.component';
import {
  ExportdJobSchedulingStepComponent
} from './exportd-job-settings-builder/exportd-job-scheduling-step/exportd-job-scheduling-step.component';
import {
  ExportdJobCompleteStepComponent
} from './exportd-job-settings-builder/exportd-job-complete-step/exportd-job-complete-step.component';
import { DndModule } from 'ngx-drag-drop';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { NgSelectModule } from '@ng-select/ng-select';
import { NgbProgressbarModule, NgbTooltipModule } from '@ng-bootstrap/ng-bootstrap';
import { DeleteLogJobModalComponent, ExportdJobLogsComponent } from './exportd-job-logs/exportd-job-logs.component';
import { ExportdJobSettingsCopyComponent } from './exportd-job-settings-copy/exportd-job-settings-copy.component';
import { AuthModule } from '../../auth/auth.module';

@NgModule({
  entryComponents: [DeleteLogJobModalComponent],
  declarations: [
    ExportdJobSettingsListComponent,
    ExportdJobSettingsEditComponent,
    ExportdJobSettingsAddComponent,
    ExportdJobSettingsBuilderComponent,
    ExportdJobBasicStepComponent,
    ExportdJobSourcesStepComponent,
    ExportdJobDestinationsStepComponent,
    ExportdJobVariablesStepComponent,
    ExportdJobSchedulingStepComponent,
    ExportdJobCompleteStepComponent,
    ExportdJobLogsComponent,
    DeleteLogJobModalComponent,
    FilterPipe,
    ExportdJobSettingsCopyComponent],
  imports: [
    CommonModule,
    LayoutModule,
    ExportdJobSettingsRoutingModule,
    DataTablesModule,
    FontAwesomeModule,
    ArchwizardModule,
    DndModule,
    ReactiveFormsModule,
    NgSelectModule,
    NgbTooltipModule,
    FormsModule,
    NgbProgressbarModule,
    AuthModule
  ]
})
export class ExportdJobSettingsModule {
}
