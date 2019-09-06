import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { CategoryListComponent } from './category-list/category-list.component';
import { CategoryManagementComponent } from './category-management/category-management.component';
import { CategoryAddComponent } from './category-add/category-add.component';

const routes: Routes = [
  {
    path: '',
    data: {
      breadcrumb: 'List'
    },
    component: CategoryListComponent
  },
  {
    path: 'management',
    data: {
      breadcrumb: 'Manage'
    },
    component: CategoryManagementComponent
  },
  {
    path: 'add',
    data: {
      breadcrumb: 'Add'
    },
    component: CategoryAddComponent
  },
  {
    path: 'edit/:publicID',
    data: {
      breadcrumb: 'Edit'
    },
    component: CategoryAddComponent
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class CategoryRoutingModule {
}
