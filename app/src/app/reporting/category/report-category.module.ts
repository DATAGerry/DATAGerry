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
        CategoryFormComponent
    ],
    imports: [
        CommonModule,
        ReportCategoryRoutingModule,
        TableModule,
        ReactiveFormsModule
    ]
})
export class ReportCategoryModule { }
