import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { RightsRoutingModule } from './rights-routing.module';
import { RightsListComponent } from './rights-list/rights-list.component';
import { DataTablesModule } from 'angular-datatables';

@NgModule({
  imports: [
    CommonModule,
    RightsRoutingModule,
    DataTablesModule
  ],
  declarations: [RightsListComponent]
})
export class RightsModule { }
