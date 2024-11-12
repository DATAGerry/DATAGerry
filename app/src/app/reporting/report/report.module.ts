import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReportRoutingModule } from './report-routing.module';
import { ReportOverviewComponent } from './components/report-overview/report-overview.component';

@NgModule({
    declarations: [
        ReportOverviewComponent
    ],
    imports: [
        CommonModule,
        ReportRoutingModule
    ]
})
export class ReportModule { }
