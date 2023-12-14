/*
* DATAGERRY - OpenSource Enterprise CMDB
* Copyright (C) 2023 becon GmbH
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
* along with this program.  If not, see <https://www.gnu.org/licenses/>.
*/
import { NgModule } from '@angular/core';

import { SectionTemplateService } from './services/section-template.service';
import { SectionTemplateComponent } from './section-template.component';
import { SectionTemplateRoutingModule } from './section-template-routing.module';
import { SectionTemplateBuilderComponent } from './layout/section-template-builder/section-template-builder.component';
import { SectionTemplateAddComponent } from './layout/section-template-add/section-template-add.component';
import { CommonModule } from '@angular/common';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { NgSelectModule } from '@ng-select/ng-select';
import { NgbDatepickerModule } from '@ng-bootstrap/ng-bootstrap';
import { DndModule } from 'ngx-drag-drop';
import { BuilderModule } from '../type/builder/builder.module';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { ToastModule } from 'src/app/layout/toast/toast.module';
import { SectionTemplateDeleteModalComponent } from './layout/modals/section-template-delete/section-template-delete-modal.component';
import { SectionTemplateTransformModalComponent } from './layout/modals/section-template-transform/section-template-transform-modal.component';
/* ------------------------------------------------------------------------------------------------------------------ */

@NgModule({
    declarations:[
      SectionTemplateComponent,
      SectionTemplateBuilderComponent,
      SectionTemplateAddComponent,
      SectionTemplateDeleteModalComponent,
      SectionTemplateTransformModalComponent
    ],
    imports: [
      SectionTemplateRoutingModule,
      CommonModule,
      FontAwesomeModule,
      FormsModule,
      ReactiveFormsModule,
      NgSelectModule,
      NgbDatepickerModule,
      DndModule,
      BuilderModule,
      MatCheckboxModule,
      ToastModule
    ],
    exports: [

    ],
    providers:[
      SectionTemplateService
    ]
})
export class SectionTemplateModule {
    
}