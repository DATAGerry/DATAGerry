/*
* DATAGERRY - OpenSource Enterprise CMDB
* Copyright (C) 2023 becon GmbH
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

import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { CommonModule, DatePipe } from '@angular/common';
import { HTTP_INTERCEPTORS, HttpClientModule } from '@angular/common/http';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

import { LayoutModule } from './layout/layout.module';
import { ToastModule } from './layout/toast/toast.module';
import { AppRoutingModule } from './app-routing.module';
import { MainModule } from './main/main.module';
import { AuthModule } from './auth/auth.module';
import { ProgressModule } from './layout/progress/progress.module';

import { PreviousRouteService } from './services/previous-route.service';
import { RequestCacheService } from './services/request-cache.service';
import { AppLoadingService } from './services/app-loading.service';
import { ProgressBarService } from './layout/progress/progress-bar.service';
import { ProgressSpinnerService } from './layout/progress/progress-spinner.service';
import { SessionTimeoutService } from './auth/services/session-timeout.service';
import { TreeManagerService } from './services/tree-manager.service';
import { ObjectService } from './framework/services/object.service';

import { HttpErrorInterceptor } from './error/interceptors/http-error.interceptor.tx';
import { BasicAuthInterceptor } from './auth/interceptors/basic-auth.interceptor';
import { APICachingInterceptor } from './services/api-cache.interceptor';

import { DateFormatterPipe } from './layout/pipes/date-formatter.pipe';

import { AppComponent } from './app.component';
/* -------------------------------------------------------------------------- */


@NgModule({
  declarations: [
    AppComponent,
  ],
  imports: [
    CommonModule,
    BrowserModule,
    BrowserAnimationsModule,
    HttpClientModule,
    MainModule,
    AuthModule,
    LayoutModule,
    ToastModule,
    ProgressModule,
    AppRoutingModule
  ],
  exports: [
    BrowserModule
  ],
  providers: [
    PreviousRouteService,
    DatePipe,
    DateFormatterPipe,
    AppLoadingService,
    SessionTimeoutService,
    ProgressBarService,
    ProgressSpinnerService,
    RequestCacheService,
    TreeManagerService,
    ObjectService,
    { provide: HTTP_INTERCEPTORS, useClass: BasicAuthInterceptor, multi: true },
    { provide: HTTP_INTERCEPTORS, useClass: HttpErrorInterceptor, multi: true },
    { provide: HTTP_INTERCEPTORS, useClass: APICachingInterceptor, multi: true }
  ],
  bootstrap: [AppComponent]
})
export class AppModule {
}
