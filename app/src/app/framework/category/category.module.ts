import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { CategoryRoutingModule } from './category-routing.module';
import { CategoryListComponent } from './category-list/category-list.component';
import { CategoryManagementComponent } from './category-management/category-management.component';
import { DndModule } from 'ngx-drag-drop';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import { LayoutModule } from '../../layout/layout.module';
import { NgSelectModule } from '@ng-select/ng-select';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { CategoryAddComponent } from './category-add/category-add.component';
import { FilterPipe } from './filter.pipe';
import { DataTablesModule } from 'angular-datatables';

@NgModule({
  declarations: [CategoryListComponent, CategoryManagementComponent, CategoryAddComponent, FilterPipe],
  imports: [
    CommonModule,
    CategoryRoutingModule,
    DndModule,
    ReactiveFormsModule,
    LayoutModule,
    NgSelectModule,
    FontAwesomeModule,
    FormsModule,
    DataTablesModule
  ]
})
export class CategoryModule {
}
