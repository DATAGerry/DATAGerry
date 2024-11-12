import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ReportRoutingModule } from './report/report-routing.module';
import { ReportCategoryRoutingModule } from './category/report-category-routing.module';

const routes: Routes = [
    {
        path: '',
        redirectTo: 'reports',
        pathMatch: 'full'
    }
];

@NgModule({
    imports: [
        RouterModule.forChild(routes),
        ReportRoutingModule,
        ReportCategoryRoutingModule
    ],
    exports: [RouterModule]
})
export class ReportingRoutingModule { }
