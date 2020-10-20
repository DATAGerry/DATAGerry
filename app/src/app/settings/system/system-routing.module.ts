import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { InformationComponent } from './information/information.component';
import { PropertiesComponent } from './properties/properties.component';

const routes: Routes = [
  {
    path: '',
    pathMatch: 'full',
    data: {
      breadcrumb: 'Information',
      right: 'base.system.view'
    },
    component: InformationComponent
  },
  {
    path: 'properties',
    data: {
      breadcrumb: 'Properties',
      right: 'base.system.reload'
    },
    component: PropertiesComponent
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class SystemRoutingModule { }
