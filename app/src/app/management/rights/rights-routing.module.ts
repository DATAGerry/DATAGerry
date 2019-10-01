import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { RightsListComponent } from './rights-list/rights-list.component';

const routes: Routes = [
  {
    path: '',
    data: {
      breadcrumb: 'List'
    },
    component: RightsListComponent
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class RightsRoutingModule {
}
