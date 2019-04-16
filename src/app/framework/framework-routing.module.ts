import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { NavigationComponent } from '../layout/components/navigation/navigation.component';
import { BreadcrumbComponent } from '../layout/components/breadcrumb/breadcrumb.component';
import { SidebarComponent } from '../layout/components/sidebar/sidebar.component';

const routes: Routes = [
  {
    path: '',
    component: NavigationComponent,
    outlet: 'navigation'
  },
  {
    path: '',
    component: SidebarComponent,
    outlet: 'sidebar'
  },
  {
    path: '',
    component: BreadcrumbComponent,
    outlet: 'breadcrumb'
  },
  {
    path: 'type',
    data: {
      breadcrumb: 'Type'
    },
    loadChildren: './type/type.module#TypeModule',
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class FrameworkRoutingModule { }
