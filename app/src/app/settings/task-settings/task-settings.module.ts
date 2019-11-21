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
import { TaskSettingsListComponent } from './task-settings-list/task-settings-list.component';
import { TaskSettingsEditComponent } from './task-settings-edit/task-settings-edit.component';
import { TaskSettingsAddComponent } from './task-settings-add/task-settings-add.component';
import { DataTablesModule } from 'angular-datatables';
import { TaskSettingsRoutingModule } from './task-settings-routing.module';
import { LayoutModule } from '../../layout/layout.module';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { TaskSettingsBuilderComponent } from './task-settings-builder/task-settings-builder.component';
import {ArchwizardModule} from 'angular-archwizard';
import { TaskBasicStepComponent } from './task-settings-builder/task-basic-step/task-basic-step.component';
import { TaskSourcesStepComponent } from './task-settings-builder/task-sources-step/task-sources-step.component';
import { TaskDestinationsStepComponent } from './task-settings-builder/task-destinations-step/task-destinations-step.component';
import { TaskVariablesStepComponent } from './task-settings-builder/task-variables-step/task-variables-step.component';
import { TaskSchedulingStepComponent } from './task-settings-builder/task-scheduling-step/task-scheduling-step.component';
import { TaskCompleteStepComponent } from './task-settings-builder/task-complete-step/task-complete-step.component';
import { DndModule } from 'ngx-drag-drop';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import { NgSelectModule } from '@ng-select/ng-select';
import {NgbTooltipModule} from "@ng-bootstrap/ng-bootstrap";
import {SweetAlert2Module} from "@sweetalert2/ngx-sweetalert2";

@NgModule({
  declarations: [
    TaskSettingsListComponent,
    TaskSettingsEditComponent,
    TaskSettingsAddComponent,
    TaskSettingsBuilderComponent,
    TaskBasicStepComponent,
    TaskSourcesStepComponent,
    TaskDestinationsStepComponent,
    TaskVariablesStepComponent,
    TaskSchedulingStepComponent,
    TaskCompleteStepComponent],
  imports: [
    CommonModule,
    LayoutModule,
    TaskSettingsRoutingModule,
    DataTablesModule,
    FontAwesomeModule,
    ArchwizardModule,
    DndModule,
    ReactiveFormsModule,
    NgSelectModule,
    NgbTooltipModule,
    FormsModule,
    SweetAlert2Module
  ]
})
export class TaskSettingsModule { }
