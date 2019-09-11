import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { YourObjectsComponent } from './your-objects/your-objects.component';
import { UserObjectsNewComponent } from './user-objects-new/user-objects-new.component';
import { UserObjectChangedComponent } from './user-object-changed/user-object-changed.component';

const routes: Routes = [
  {
    path: 'own',
    data: {
      breadcrumb: 'Your Objects'
    },
    component: YourObjectsComponent
  }, {
    path: 'new',
    data: {
      breadcrumb: 'New Objects'
    },
    component: UserObjectsNewComponent
  }, {
    path: 'changed',
    data: {
      breadcrumb: 'Changed Objects'
    },
    component: UserObjectChangedComponent
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class UserObjectRoutingModule {
}
