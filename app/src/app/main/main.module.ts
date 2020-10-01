import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { MainRoutingModule } from './main-routing.module';
import { MainComponent } from './main.component';
import { AuthModule } from '../auth/auth.module';
import { FileSaverModule } from 'ngx-filesaver';
import { LayoutModule } from '../layout/layout.module';
import { ToastModule } from '../layout/toast/toast.module';


@NgModule({
  declarations: [
    MainComponent
  ],
  imports: [
    CommonModule,
    MainRoutingModule,
    AuthModule,
    LayoutModule,
    FileSaverModule,
    ToastModule
  ],
  exports: [
    MainComponent
  ]
})
export class MainModule {
}
