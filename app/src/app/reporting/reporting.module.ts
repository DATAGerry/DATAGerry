import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReportingRoutingModule } from './reporting-routing.module';

// Import the feature modules
import { ReportModule } from './report/report.module';
import { ReportCategoryModule } from './category/report-category.module';

@NgModule({
    declarations: [],
    imports: [
        CommonModule,
        ReportingRoutingModule, // Main routing module for reporting
        ReportModule,
        ReportCategoryModule
    ]
})
export class ReportingModule { }
