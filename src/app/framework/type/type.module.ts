import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { TypeViewComponent } from './components/type-view/type-view.component';
import { TypeListComponent } from './components/type-list/type-list.component';
import { TypeRoutingModule } from './type-routing.module';

@NgModule({
  declarations: [TypeViewComponent, TypeListComponent],
  imports: [
    CommonModule,
    TypeRoutingModule
  ]
})
export class TypeModule { }
