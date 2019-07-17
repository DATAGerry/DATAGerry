import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { CategoryListComponent } from './components/category-list/category-list.component';

const routes: Routes = [
  {
    path: '',
    data: {
      breadcrumb: 'List'
    },
    component: CategoryListComponent
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class CategoryRoutingModule {
}
