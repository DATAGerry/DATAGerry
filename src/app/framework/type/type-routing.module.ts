import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { TypeViewComponent } from './components/type-view/type-view.component';
import { TypeListComponent } from './components/type-list/type-list.component';
import { TypeAddComponent } from './components/type-add/type-add.component';

const routes: Routes = [
  {
    path: '',
    data: {
      breadcrumb: 'List'
    },
    component: TypeListComponent
  },
  {
    path: 'add',
    data: {
      breadcrumb: 'Add'
    },
    component: TypeAddComponent
  },
  {
    path: ':publicID',
    component: TypeViewComponent
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class TypeRoutingModule { }
