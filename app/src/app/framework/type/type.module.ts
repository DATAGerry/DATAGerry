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
import { TypeRoutingModule } from './type-routing.module';
import { LayoutModule } from '../../layout/layout.module';
import { DataTablesModule } from 'angular-datatables';
import { TypeAddComponent } from './type-add/type-add.component';
import { ArchwizardModule } from 'angular-archwizard';
import { TypeBuilderComponent } from './type-builder/type-builder.component';
import { TypeBasicStepComponent } from './type-builder/type-basic-step/type-basic-step.component';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { TypeFieldsStepComponent } from './type-builder/type-fields-step/type-fields-step.component';
import { QRCodeModule } from 'angularx-qrcode';
import { NgSelectModule } from '@ng-select/ng-select';
import { TypeValidationStepComponent } from './type-builder/type-validation-step/type-validation-step.component';
import { RenderModule } from '../render/render.module';
import { BuilderModule } from './builder/builder.module';
import { TypeEditComponent } from './type-edit/type-edit.component';
import { TypeMetaStepComponent } from './type-builder/type-meta-step/type-meta-step.component';
import { TypeDeleteComponent, TypeDeleteConfirmModalComponent } from './type-delete/type-delete.component';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { AuthModule } from '../../auth/auth.module';
import { TypeComponent } from './type.component';
import { CleanupModalComponent } from './modals/cleanup-modal/cleanup-modal.component';
import { CleanButtonComponent } from './components/clean-button/clean-button.component';
import { TypeAclStepComponent } from './type-builder/type-acl-step/type-acl-step.component';
import { GroupsAclTabsComponent } from './type-builder/type-acl-step/groups-acl-tabs/groups-acl-tabs.component';
import { TableModule } from '../../layout/table/table.module';
import { TypeTableActionsComponent } from './components/type-table-actions/type-table-actions.component';

@NgModule({
  entryComponents: [TypeDeleteConfirmModalComponent, CleanupModalComponent],
  declarations: [
    TypeAddComponent,
    TypeBasicStepComponent,
    TypeFieldsStepComponent,
    TypeBuilderComponent,
    TypeValidationStepComponent,
    TypeEditComponent,
    TypeMetaStepComponent,
    TypeDeleteComponent,
    TypeDeleteConfirmModalComponent,
    TypeComponent,
    CleanupModalComponent,
    CleanButtonComponent,
    TypeAclStepComponent,
    GroupsAclTabsComponent,
    TypeTableActionsComponent
  ],
    imports: [
        CommonModule,
        TypeRoutingModule,
        DataTablesModule,
        LayoutModule,
        ReactiveFormsModule,
        ArchwizardModule,
        QRCodeModule,
        NgSelectModule,
        RenderModule,
        BuilderModule,
        FormsModule,
        NgbModule,
        FontAwesomeModule,
        AuthModule,
        TableModule
    ]
})
export class TypeModule {
}
