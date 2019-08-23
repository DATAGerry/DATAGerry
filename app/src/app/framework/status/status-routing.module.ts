import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { StatusListComponent } from './status-list/status-list.component';
import { StatusAddComponent } from './status-add/status-add.component';
import { StatusEditComponent } from './status-edit/status-edit.component';

const routes: Routes = [
  {
    path: '',
    component: StatusListComponent
  },
  {
    path: 'add',
    component: StatusAddComponent
  },
  {
    path: 'edit/:publicID',
    component: StatusEditComponent
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class StatusRoutingModule { }
