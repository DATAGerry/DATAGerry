/*
* dataGerry - OpenSource Enterprise CMDB
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
import { BasicAuthInterceptor } from './auth/interceptors/basic-auth.interceptor';
import { HttpErrorInterceptor } from './auth/interceptors/http-error.interceptor.tx';
import { PreviousRouteService } from './services/previous-route.service';
import { NgxSpinnerModule } from 'ngx-spinner';
import { ConnectionService } from './services/connection.service';
import { DatePipe } from '@angular/common';
import { FileSaverModule } from 'ngx-filesaver';

@NgModule({
  declarations: [
    AppComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    LayoutModule,
    NgxSpinnerModule,
    AppRoutingModule,
    FileSaverModule
  ],
  providers: [
    PreviousRouteService,
    ConnectionService,
    DatePipe,
    {provide: HTTP_INTERCEPTORS, useClass: BasicAuthInterceptor, multi: true},
    //{provide: HTTP_INTERCEPTORS, useClass: HttpErrorInterceptor, multi: true},
  ],
  bootstrap: [AppComponent]
})
export class AppModule {
}
