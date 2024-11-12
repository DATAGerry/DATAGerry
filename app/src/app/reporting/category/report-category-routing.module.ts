import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { CategoryOverviewComponent } from './components/category-overview/category-overview.component';
import { CategoryFormComponent } from './components/category-form/category-form.component';

const routes: Routes = [
    {
        path: 'categories',
        component: CategoryOverviewComponent
    },
    {
        path: 'categories/add',
        component: CategoryFormComponent
    },
    {
        path: 'categories/edit/:categoryID',
        component: CategoryFormComponent
    }
];

@NgModule({
    imports: [RouterModule.forChild(routes)],
    exports: [RouterModule]
})
export class ReportCategoryRoutingModule { }
