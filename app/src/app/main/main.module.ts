/*
* DATAGERRY - OpenSource Enterprise CMDB
* Copyright (C) 2024 becon GmbH
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
*
* You should have received a copy of the GNU Affero General Public License
* along with this program. If not, see <https://www.gnu.org/licenses/>.
*/
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { NgxIndexedDBModule } from 'ngx-indexed-db';

import { userSettingsDBConfig } from '../management/user-settings/user-settings.module';
import { MainRoutingModule } from './main-routing.module';
import { DashboardModule } from '../modules/dashboard/dashboard.module';

import { UserSettingsDBService } from '../management/user-settings/services/user-settings-db.service';
import { UserSettingsService } from '../management/user-settings/services/user-settings.service';
import { DateSettingsService } from '../settings/services/date-settings.service';


/* ------------------------------------------------------------------------------------------------------------------ */

@NgModule({
    imports: [
        CommonModule,
        NgxIndexedDBModule.forRoot(userSettingsDBConfig),
        MainRoutingModule,
        DashboardModule
    ],
    providers: [
        UserSettingsDBService,
        UserSettingsService,
        DateSettingsService
    ]
})
export class MainModule {
    constructor(private dateSettingsService: DateSettingsService) {

    }
}
