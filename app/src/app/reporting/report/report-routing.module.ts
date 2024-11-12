import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ReportOverviewComponent } from './components/report-overview/report-overview.component';

const routes: Routes = [
    { path: '', component: ReportOverviewComponent }, // Default path for report overview
];

@NgModule({
    imports: [RouterModule.forChild(routes)],
    exports: [RouterModule]
})
export class ReportRoutingModule { }
