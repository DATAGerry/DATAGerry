import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { TypeViewComponent } from './components/type-view/type-view.component';
import { TypeListComponent } from './components/type-list/type-list.component';
import { TypeRoutingModule } from './type-routing.module';
import { LayoutModule } from '../../layout/layout.module';
import { DataTablesModule } from 'angular-datatables';
import { TypeAddComponent } from './components/type-add/type-add.component';

@NgModule({
  declarations: [TypeViewComponent, TypeListComponent, TypeAddComponent],
  imports: [
    CommonModule,
    TypeRoutingModule,
    DataTablesModule,
    LayoutModule,
  ]
})
export class TypeModule { }
