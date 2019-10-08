import { NgModule } from '@angular/core';

import { CommonModule } from '@angular/common';
import { UsersRoutingModule } from './users-routing.module';
import { UsersListComponent } from './users-list/users-list.component';
import { DataTablesModule } from 'angular-datatables';
import { UsersAddComponent } from './users-add/users-add.component';
import { PasswordStrengthMeterModule } from '../../layout/password-strength-meter/password-strength-meter.module';
import { ReactiveFormsModule } from '@angular/forms';
import { UserViewComponent } from './user-view/user-view.component';
import { LayoutModule } from '../../layout/layout.module';
import { UsersEditComponent } from './users-edit/users-edit.component';

@NgModule({
  declarations: [UsersListComponent, UserViewComponent, UsersAddComponent, UsersEditComponent],
  imports: [
    CommonModule,
    UsersRoutingModule,
    DataTablesModule,
    PasswordStrengthMeterModule,
    ReactiveFormsModule,
    LayoutModule,
  ]
})
export class UsersModule { }
