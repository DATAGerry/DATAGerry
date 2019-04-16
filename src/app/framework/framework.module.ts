import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FrameworkRoutingModule } from './framework-routing.module';
import { LayoutModule } from '../layout/layout.module';

@NgModule({
  imports: [
    CommonModule,
    LayoutModule,
    FrameworkRoutingModule
  ]
})
export class FrameworkModule { }
