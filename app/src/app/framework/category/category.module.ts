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
* along with this program. If not, see <https://www.gnu.org/licenses/>.
*/

import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { CategoryRoutingModule } from './category-routing.module';
import { DndModule } from 'ngx-drag-drop';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { LayoutModule } from '../../layout/layout.module';
import { NgSelectModule } from '@ng-select/ng-select';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { CategoryComponent } from './category.component';
import { CategoryAddComponent } from './category-add/category-add.component';
import { CategoryFormComponent } from './category-form/category-form.component';
import { IconPickerModule } from 'ngx-icon-picker';
import { CategoryEditComponent } from './category-edit/category-edit.component';
import { CategoryTreeComponent } from './components/category-tree/category-tree.component';
import { CategoryNodeComponent } from './components/category-node/category-node.component';
import { CategoryDeleteComponent } from './category-delete/category-delete.component';
import { AuthModule } from '../../auth/auth.module';
import { AddCategoryModalComponent } from './components/modals/add-category-modal/add-category-modal.component';
import { CategoryViewComponent } from './category-view/category-view.component';

@NgModule({
  declarations: [CategoryComponent, CategoryAddComponent, CategoryFormComponent, CategoryEditComponent, CategoryTreeComponent, CategoryNodeComponent, AddCategoryModalComponent, CategoryDeleteComponent, CategoryViewComponent],
  imports: [
    CommonModule,
    CategoryRoutingModule,
    DndModule,
    ReactiveFormsModule,
    LayoutModule,
    NgSelectModule,
    FontAwesomeModule,
    FormsModule,
    IconPickerModule,
    AuthModule
  ],
  entryComponents: [AddCategoryModalComponent, CategoryDeleteComponent]
})
export class CategoryModule {
}
