import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { RightsRoutingModule } from './rights-routing.module';
import { RightsListComponent } from './rights-list/rights-list.component';
import { DataTablesModule } from 'angular-datatables';
import { RightLevelColorDirective } from './right-level-color.directive';

@NgModule({
  imports: [
    CommonModule,
    RightsRoutingModule,
    DataTablesModule
  ],
  declarations: [RightsListComponent, RightLevelColorDirective]
})
export class RightsModule { }
