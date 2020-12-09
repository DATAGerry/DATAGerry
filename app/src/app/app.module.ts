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

import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { LayoutModule } from './layout/layout.module';
import { HTTP_INTERCEPTORS, HttpClientModule } from '@angular/common/http';
import { PreviousRouteService } from './services/previous-route.service';
import { DatePipe } from '@angular/common';
import { ToastModule } from './layout/toast/toast.module';
import { HttpErrorInterceptor } from './error/interceptors/http-error.interceptor.tx';
import { BasicAuthInterceptor } from './auth/interceptors/basic-auth.interceptor';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MainModule } from './main/main.module';
import { AuthModule } from './auth/auth.module';
import { APICachingInterceptor } from './services/api-cache.interceptor';
import { RequestCacheService } from './services/request-cache.service';
import { ProgressModule } from './layout/progress/progress.module';
import { AppLoadingService } from './services/app-loading.service';
import { ProgressBarService } from './layout/progress/progress-bar.service';
import { ProgressSpinnerService } from './layout/progress/progress-spinner.service';

@NgModule({
  declarations: [
    AppComponent,
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    HttpClientModule,
    MainModule,
    AuthModule,
    LayoutModule,
    ToastModule,
    AppRoutingModule,
    ProgressModule
  ],
  providers: [
    PreviousRouteService,
    DatePipe,
    AppLoadingService,
    ProgressBarService,
    ProgressSpinnerService,
    RequestCacheService,
    { provide: HTTP_INTERCEPTORS, useClass: BasicAuthInterceptor, multi: true },
    { provide: HTTP_INTERCEPTORS, useClass: HttpErrorInterceptor, multi: true },
    { provide: HTTP_INTERCEPTORS, useClass: APICachingInterceptor, multi: true }
  ],
  bootstrap: [AppComponent]
})
export class AppModule {
}
