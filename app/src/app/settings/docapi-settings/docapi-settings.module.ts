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
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { EditorModule } from '@tinymce/tinymce-angular';
import { ArchwizardModule } from 'angular-archwizard';
import { LayoutModule } from '../../layout/layout.module';
import { AuthModule } from "../../auth/auth.module";
import { DocapiSettingsRoutingModule } from './docapi-settings-routing.module';
import { DocapiSettingsListComponent } from './docapi-settings-list/docapi-settings-list.component';
import { DocapiSettingsBuilderComponent } from './docapi-settings-builder/docapi-settings-builder.component';
import { DocapiSettingsAddComponent } from './docapi-settings-add/docapi-settings-add.component';
import { DocapiSettingsBuilderSettingsStepComponent } from './docapi-settings-builder/docapi-settings-builder-settings-step/docapi-settings-builder-settings-step.component';
import { DocapiSettingsBuilderContentStepComponent } from './docapi-settings-builder/docapi-settings-builder-content-step/docapi-settings-builder-content-step.component';

@NgModule({
  declarations: [DocapiSettingsListComponent, DocapiSettingsBuilderComponent, DocapiSettingsAddComponent, DocapiSettingsBuilderSettingsStepComponent, DocapiSettingsBuilderContentStepComponent],
  imports: [
    CommonModule,
    EditorModule,
    FormsModule,
    ReactiveFormsModule,
    ArchwizardModule,
    LayoutModule,
    AuthModule,
    DocapiSettingsRoutingModule
  ]
})
export class DocapiSettingsModule { }
