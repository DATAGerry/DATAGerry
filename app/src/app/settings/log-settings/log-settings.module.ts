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

import { LogSettingsRoutingModule } from './log-settings-routing.module';
import { DeleteModalComponent, LogObjectSettingsComponent } from './log-object-settings/log-object-settings.component';
import { ActivateTabComponent } from './log-object-settings/activate-tab/activate-tab.component';
import { DeactivateTabComponent } from './log-object-settings/deactivate-tab/deactivate-tab.component';
import { DeleteTabComponent } from './log-object-settings/delete-tab/delete-tab.component';
import { DataTablesModule } from 'angular-datatables';
import { LayoutModule } from '../../layout/layout.module';
import { NgbProgressbarModule, NgbTooltipModule } from '@ng-bootstrap/ng-bootstrap';

@NgModule({
  entryComponents: [DeleteModalComponent],
  declarations: [DeleteModalComponent, LogObjectSettingsComponent, ActivateTabComponent, DeactivateTabComponent, DeleteTabComponent],
  imports: [
    CommonModule,
    LayoutModule,
    LogSettingsRoutingModule,
    DataTablesModule,
    NgbTooltipModule,
    NgbProgressbarModule
  ]
})
export class LogSettingsModule {
}
