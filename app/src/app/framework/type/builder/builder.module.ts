/*
* DATAGERRY - OpenSource Enterprise CMDB
* Copyright (C) 2019 - 2021 NETHINKS GmbH
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
* along with this program. If not, see <https://www.gnu.org/licenses/>.
*/

import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { BuilderComponent } from './builder.component';
import { DndModule } from 'ngx-drag-drop';
import { RenderModule } from '../../render/render.module';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { NgSelectModule } from '@ng-select/ng-select';
import { TextFieldEditComponent } from './configs/edits/text-field-edit.component';
import { SectionFieldEditComponent } from './configs/edits/section-field-edit.component';
import { TextareaEditComponent } from './configs/edits/textarea-edit.component';
import { RefFieldEditComponent } from './configs/edits/ref-field-edit.component';
import { ChoiceFieldEditComponent } from './configs/edits/choice-field-edit.component';
import { CheckFieldEditComponent } from './configs/edits/check-field-edit.component';
import { NgbDatepickerModule, NgbModalModule, NgbTooltipModule } from '@ng-bootstrap/ng-bootstrap';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { DateFieldEditComponent } from './configs/edits/date-field-edit.component';
import { CategoryModule } from '../../category/category.module';
import { SectionRefFieldEditComponent } from './configs/edits/section-ref-field-edit.component';
import { LayoutModule } from '../../../layout/layout.module';
import { ConfigEditBaseComponent } from './configs/config.edit';
import { ConfigEditComponent } from './configs/config-edit.component';

@NgModule({
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
    CategoryModule,
    NgbTooltipModule,
    LayoutModule
  ],
  declarations: [
    ConfigEditBaseComponent,
    ConfigEditComponent,
    BuilderComponent,
    TextFieldEditComponent,
    SectionFieldEditComponent,
    TextareaEditComponent,
    RefFieldEditComponent,
    ChoiceFieldEditComponent,
    CheckFieldEditComponent,
    DateFieldEditComponent,
    SectionRefFieldEditComponent,
  ],
  exports: [
    BuilderComponent
  ]
})
export class BuilderModule {
}
