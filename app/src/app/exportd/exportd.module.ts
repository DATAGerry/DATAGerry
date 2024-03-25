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
*
* You should have received a copy of the GNU Affero General Public License
* along with this program. If not, see <https://www.gnu.org/licenses/>.
*/
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';

import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { ArchwizardModule } from '@rg-software/angular-archwizard';
import { DndModule } from 'ngx-drag-drop';
import { NgSelectModule } from '@ng-select/ng-select';
import { NgbProgressbarModule, NgbTooltipModule } from '@ng-bootstrap/ng-bootstrap';

import { AuthModule } from '../auth/auth.module';
import { TableModule } from '../layout/table/table.module';
import { UsersModule } from '../management/users/users.module';
import { LogSettingsModule } from '../settings/log-settings/log-settings.module';
import { RenderModule } from '../framework/render/render.module';
import { ExportdRoutingModule } from './exportd-routing.module';
import { LayoutModule } from '../layout/layout.module';

import { ExportdJobSettingsListComponent } from './exportd-job-settings-list/exportd-job-settings-list.component';
import { ExportdJobSettingsEditComponent } from './exportd-job-settings-edit/exportd-job-settings-edit.component';
import { ExportdJobSettingsAddComponent } from './exportd-job-settings-add/exportd-job-settings-add.component';
import {
    ExportdJobSettingsBuilderComponent
} from './exportd-job-settings-builder/exportd-job-settings-builder.component';
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
    DropDownDirectionDirective,
    ExportdJobVariablesStepComponent,
    FilterPipe
} from './exportd-job-settings-builder/exportd-job-variables-step/exportd-job-variables-step.component';
import {
    ExportdJobSchedulingStepComponent
} from './exportd-job-settings-builder/exportd-job-scheduling-step/exportd-job-scheduling-step.component';
import {
    ExportdJobCompleteStepComponent
} from './exportd-job-settings-builder/exportd-job-complete-step/exportd-job-complete-step.component';
import { ExportdJobLogsComponent } from './exportd-job-logs/exportd-job-logs.component';
import { ExportdJobSettingsCopyComponent } from './exportd-job-settings-copy/exportd-job-settings-copy.component';
import { ExportdJobBaseStepComponent } from './exportd-job-settings-builder/exportd-job-base-step.component';
/* ------------------------------------------------------------------------------------------------------------------ */

@NgModule({
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
        FilterPipe,
        ExportdJobSettingsCopyComponent,
        DropDownDirectionDirective,
        ExportdJobBaseStepComponent
    ],
    imports: [
        CommonModule,
        ExportdRoutingModule,
        LayoutModule,
        FontAwesomeModule,
        ArchwizardModule,
        DndModule,
        ReactiveFormsModule,
        NgSelectModule,
        NgbTooltipModule,
        FormsModule,
        NgbProgressbarModule,
        AuthModule,
        TableModule,
        UsersModule,
        LogSettingsModule,
        RenderModule
    ]
})
export class ExportdModule {
}
