import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { UsersListComponent } from './users-list/users-list.component';
import { UsersAddComponent } from './users-add/users-add.component';
import { UserViewComponent } from './user-view/user-view.component';
import { UsersEditComponent } from './users-edit/users-edit.component';

const routes: Routes = [
  {
    path: '',
    data: {
      breadcrumb: 'List'
    },
    component: UsersListComponent
  },
  {
    path: 'add',
    data: {
      breadcrumb: 'Add'
    },
    component: UsersAddComponent
  },
  {
    path: 'view/:publicID',
    data: {
      breadcrumb: 'View'
    },
    component: UserViewComponent
  },
  {
    path: 'edit/:publicID',
    data: {
      breadcrumb: 'Edit'
    },
    component: UsersEditComponent
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class UsersRoutingModule {
}
