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

import { MainRoutingModule } from './main-routing.module';
import { FileSaverModule } from 'ngx-filesaver';
import { LayoutModule } from '../layout/layout.module';
import { ToastModule } from '../layout/toast/toast.module';
import { DashboardModule } from '../dashboard/dashboard.module';
import { UserSettingsService } from '../management/user-settings/services/user-settings.service';
import { NgxIndexedDBModule } from 'ngx-indexed-db';
import { userSettingsDBConfig } from '../management/user-settings/user-settings.module';
import { UserSetting } from '../management/user-settings/models/user-setting';


@NgModule({
  declarations: [],
  exports: [],
  imports: [
    CommonModule,
    NgxIndexedDBModule.forRoot(userSettingsDBConfig),
    MainRoutingModule,
    DashboardModule,
    LayoutModule,
    FileSaverModule,
    ToastModule
  ]
})
export class MainModule {
  public constructor(private userSettingsService: UserSettingsService) {
    const cleanUP = this.userSettingsService.cleanUserSettings().subscribe((success: boolean) => {
        console.log(`Cleaned user settings: ${ success }`);
      }, error => {
        console.error(`Error while cleaning user settings ${ error }`);
      },
      () => {
        cleanUP.unsubscribe();
      });
    this.userSettingsService.getUserSettings().subscribe((settings: Array<UserSetting>) => {
      for (const setting of settings) {
        this.userSettingsService.addUserSetting(setting);
      }
    });
  }
}
