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

* You should have received a copy of the GNU Affero General Public License
* along with this program. If not, see <https://www.gnu.org/licenses/>.
*/
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReportCategoryRoutingModule } from './report-category-routing.module';
import { CategoryOverviewComponent } from './components/category-overview/category-overview.component';
import { CategoryFormComponent } from './components/category-form/category-form.component';
import { TableModule } from "../../layout/table/table.module";
import { ReactiveFormsModule } from '@angular/forms';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap'; // Import NgbModule
import { AddCategoryModalComponent } from './components/category-add-modal/category-add-modal.component';


@NgModule({
    declarations: [
        CategoryOverviewComponent,
        CategoryFormComponent,
        AddCategoryModalComponent
    ],
    imports: [
        CommonModule,
        ReportCategoryRoutingModule,
        TableModule,
        NgbModule,
        ReactiveFormsModule
    ]
})
export class ReportCategoryModule { }
