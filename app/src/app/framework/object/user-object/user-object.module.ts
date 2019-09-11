import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { UserObjectRoutingModule } from './user-object-routing.module';
import { YourObjectsComponent } from './your-objects/your-objects.component';
import { DataTablesModule } from 'angular-datatables';
import { UserObjectsNewComponent } from './user-objects-new/user-objects-new.component';
import { UserObjectChangedComponent } from './user-object-changed/user-object-changed.component';

@NgModule({
  declarations: [YourObjectsComponent, UserObjectsNewComponent, UserObjectChangedComponent],
  imports: [
    CommonModule,
    UserObjectRoutingModule,
    DataTablesModule
  ]
})
export class UserObjectModule { }
