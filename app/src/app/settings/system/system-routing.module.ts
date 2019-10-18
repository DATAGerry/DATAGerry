import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { InformationComponent } from './information/information.component';
import { PropertiesComponent } from './properties/properties.component';
import { ServerComponent } from './server/server.component';

const routes: Routes = [
  {
    path: '',
    data: {
      breadcrumb: 'Information'
    },
    component: InformationComponent
  },
  {
    path: 'server',
    data: {
      breadcrumb: 'Server'
    },
    component: ServerComponent
  },
  {
    path: 'properties',
    data: {
      breadcrumb: 'Properties'
    },
    component: PropertiesComponent
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class SystemRoutingModule { }
