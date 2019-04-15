import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { ConnectionComponent } from './connection/connection.component';
import { AuthComponent } from './auth/auth.component';
import { ConnectionGuard } from './connection/guards/connection.guard';

const routes: Routes = [
  {
    path: 'connection',
    component: ConnectionComponent
  },
  {
    path: 'login',
    canActivate: [ConnectionGuard],
    component: AuthComponent
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {
}
