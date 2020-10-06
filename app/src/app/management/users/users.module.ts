/*
* DATAGERRY - OpenSource Enterprise CMDB
* Copyright (C) 2019 NETHINKS GmbH
*
* This program is free software: you can redistribute it and/or modify
* it under the terms of the GNU Affero General Public License as
* published by the Free Software Foundation, either version 3 of the
* License, or (at your option) any later version.
*
* This program is distributed in the hope that it will be useful,
* but WITHOUT ANY WARRANTY; without even the implied warranty of
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
* GNU Affero General Public License for more details.

* You should have received a copy of the GNU Affero General Public License
* along with this program.  If not, see <https://www.gnu.org/licenses/>.
*/

import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { UsersRoutingModule } from './users-routing.module';
import { DataTablesModule } from 'angular-datatables';
import { UsersAddComponent } from './users-add/users-add.component';
import { PasswordStrengthMeterModule } from '../../layout/password-strength-meter/password-strength-meter.module';
import { ReactiveFormsModule } from '@angular/forms';
import { UserViewComponent } from './user-view/user-view.component';
import { LayoutModule } from '../../layout/layout.module';
import { UsersEditComponent } from './users-edit/users-edit.component';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { UsersDeleteComponent } from './users-delete/users-delete.component';
import { UsersPasswdModalComponent } from './modals/users-passwd-modal/users-passwd-modal.component';
import { UsersComponent } from './users.component';
import { UserHeadlineComponent } from './components/user-headline/user-headline.component';
import { UserDisplayNameComponent } from './components/user-display-name/user-display-name.component';
import { UserImageComponent } from './components/user-image/user-image.component';
import { UserDisplayComponent } from './components/user-display/user-display.component';
import { UsersTableComponent } from './components/users-table/users-table.component';

@NgModule({
  entryComponents: [
    UsersPasswdModalComponent
  ],
  declarations: [
    UserViewComponent,
    UsersAddComponent,
    UsersEditComponent,
    UsersDeleteComponent,
    UsersPasswdModalComponent,
    UsersComponent,
    UserImageComponent,
    UserHeadlineComponent,
    UserDisplayNameComponent,
    UserDisplayComponent,
    UsersTableComponent
  ],
  exports: [
    UserImageComponent,
    UserDisplayComponent
  ],
  imports: [
    CommonModule,
    UsersRoutingModule,
    DataTablesModule,
    PasswordStrengthMeterModule,
    ReactiveFormsModule,
    LayoutModule,
    FontAwesomeModule,
  ]
})
export class UsersModule {
}
