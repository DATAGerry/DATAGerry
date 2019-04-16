import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { ConnectionComponent } from './connection/connection.component';
import { AuthComponent } from './auth/auth.component';
import { ConnectionGuard } from './connection/guards/connection.guard';

const routes: Routes = [
  {
    path: '',
    pathMatch: 'full',
    canActivate: [ConnectionGuard],
    data: {
      breadcrumb: 'Dashboard'
    },
    loadChildren: './dashboard/dashboard.module#DashboardModule'
  },
  {
    path: 'connection',
    component: ConnectionComponent
  },
  {
    path: 'login',
    canActivate: [ConnectionGuard],
    component: AuthComponent
  },
  {
    path: 'framework',
    data: {
      breadcrumb: 'Framework'
    },
    canActivate: [ConnectionGuard],
    loadChildren: './framework/framework.module#FrameworkModule'
  },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {
}
