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
import { BuilderComponent } from './builder.component';
import { DndModule } from 'ngx-drag-drop';
import { RenderModule } from '../../render/render.module';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import { NgSelectModule } from '@ng-select/ng-select';
import { ConfigEditComponent } from './configs/config-edit.component';
import { TextFieldEditComponent } from './configs/edits/text-field-edit.component';
import { DummyFieldEditComponent } from './configs/edits/dummy-field-edit.component';
import { SectionFieldEditComponent } from './configs/edits/section-field-edit.component';
import { TextareaEditComponent } from './configs/edits/textarea-edit.component';
import { RefFieldEditComponent } from './configs/edits/ref-field-edit.component';
import { ChoiceFieldEditComponent } from './configs/edits/choice-field-edit.component';
import { CheckFieldEditComponent } from './configs/edits/check-field-edit.component';
import { PreviewModalComponent } from './modals/preview-modal/preview-modal.component';
import { DiagnosticModalComponent } from './modals/diagnostic-modal/diagnostic-modal.component';
import {NgbDatepickerModule, NgbModalModule} from '@ng-bootstrap/ng-bootstrap';
import { RenderElementComponent } from '../../render/render-element/render-element.component';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { DateFieldEditComponent } from './configs/edits/date-field-edit.component';
import { AddCategoryModalComponent } from '../../category/components/modals/add-category-modal/add-category-modal.component';
import { CategoryModule } from '../../category/category.module';

@NgModule({
  entryComponents: [
    SectionFieldEditComponent,
    TextFieldEditComponent,
    TextareaEditComponent,
    RefFieldEditComponent,
    DummyFieldEditComponent,
    ChoiceFieldEditComponent,
    CheckFieldEditComponent,
    DateFieldEditComponent,
    PreviewModalComponent,
    DiagnosticModalComponent,
    AddCategoryModalComponent,
    RenderElementComponent,
  ],
  declarations: [
    BuilderComponent,
    ConfigEditComponent,
    TextFieldEditComponent,
    DummyFieldEditComponent,
    SectionFieldEditComponent,
    TextareaEditComponent,
    RefFieldEditComponent,
    ChoiceFieldEditComponent,
    CheckFieldEditComponent,
    PreviewModalComponent,
    DiagnosticModalComponent,
    DateFieldEditComponent,
  ],
  imports: [
    CommonModule,
    DndModule,
    FormsModule,
    RenderModule,
    NgbModalModule,
    NgSelectModule,
    FontAwesomeModule,
    NgbDatepickerModule,
    ReactiveFormsModule,
    CategoryModule
  ],
  exports: [
    BuilderComponent
  ]
})
export class BuilderModule {
}
