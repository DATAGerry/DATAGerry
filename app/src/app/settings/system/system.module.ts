import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { SystemRoutingModule } from './system-routing.module';
import { InformationComponent } from './information/information.component';
import { PropertiesComponent } from './properties/properties.component';
import { DataTablesModule } from 'angular-datatables';

@NgModule({
  declarations: [InformationComponent, PropertiesComponent],
  imports: [
    CommonModule,
    SystemRoutingModule,
    DataTablesModule
  ]
})
export class SystemModule { }
