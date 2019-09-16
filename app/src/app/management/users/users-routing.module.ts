import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { UsersListComponent } from './users-list/users-list.component';
import { UsersAddComponent } from './users-add/users-add.component';
import { UserViewComponent } from './user-view/user-view.component';

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
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class UsersRoutingModule {
}
