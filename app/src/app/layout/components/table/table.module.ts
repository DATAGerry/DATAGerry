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
import { ActionViewComponent } from './components/actions/action-view/action-view.component';
import { ActionEditComponent } from './components/actions/action-edit/action-edit.component';
import { ActionDeleteComponent } from './components/actions/action-delete/action-delete.component';
import { ActionsComponent } from './components/actions/actions.component';
import { RouterModule } from '@angular/router';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { AuthModule } from '../../../auth/auth.module';
import { ActionCopyComponent } from './components/actions/action-copy/action-copy.component';

@NgModule({
  declarations: [
    ActionViewComponent,
    ActionEditComponent,
    ActionDeleteComponent,
    ActionsComponent,
    ActionCopyComponent
  ],
  exports: [
    ActionsComponent
  ],
  imports: [
    CommonModule,
    RouterModule,
    FontAwesomeModule,
    AuthModule
  ]
})
export class TableModule {
}
