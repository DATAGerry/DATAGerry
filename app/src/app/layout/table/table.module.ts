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
import { TableComponent } from './table.component';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { TableHeadComponent } from './header/table-head/table-head.component';
import { TableBodyComponent } from './body/table-body/table-body.component';
import { TableSearchComponent } from './components/table-search/table-search.component';
import { TableHeaderComponent } from './header/table-header/table-header.component';
import { TablePageSizeComponent } from './components/table-page-size/table-page-size.component';


@NgModule({
  declarations: [TableComponent, TableHeadComponent, TableBodyComponent, TableSearchComponent, TableHeaderComponent, TablePageSizeComponent],
  exports: [
    TableComponent
  ],
  imports: [
    CommonModule,
    FormsModule,
    ReactiveFormsModule
  ]
})
export class TableModule {
}
