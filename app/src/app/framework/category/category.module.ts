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

import { CategoryRoutingModule } from './category-routing.module';
import { CategoryListComponent } from './category-list/category-list.component';
import { DndModule } from 'ngx-drag-drop';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { LayoutModule } from '../../layout/layout.module';
import { NgSelectModule } from '@ng-select/ng-select';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { CategoryAddComponent } from './category-add/category-add.component';
import { FilterPipe } from './filter.pipe';
import { DataTablesModule } from 'angular-datatables';
import { CategoryEditComponent } from './category-edit/category-edit.component';
import { BuildCategoryFormComponent } from './build-category-form/build-category-form.component';
import { SweetAlert2Module } from '@sweetalert2/ngx-sweetalert2';

@NgModule({
  declarations: [
    CategoryListComponent,
    CategoryAddComponent,
    FilterPipe,
    CategoryEditComponent,
    BuildCategoryFormComponent],
  exports: [
    FilterPipe
  ],
  imports: [
    CommonModule,
    CategoryRoutingModule,
    DndModule,
    ReactiveFormsModule,
    LayoutModule,
    NgSelectModule,
    FontAwesomeModule,
    FormsModule,
    DataTablesModule,
    SweetAlert2Module
  ]
})
export class CategoryModule {
}
