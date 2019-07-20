import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { CategoryRoutingModule } from './category-routing.module';
import { CategoryListComponent } from './category-list/category-list.component';
import { CategoryManagementComponent } from './category-management/category-management.component';
import { DndModule } from 'ngx-drag-drop';
import { ReactiveFormsModule } from '@angular/forms';
import { LayoutModule } from '../../layout/layout.module';
import { NgSelectModule } from '@ng-select/ng-select';

@NgModule({
  declarations: [CategoryListComponent, CategoryManagementComponent],
  imports: [
    CommonModule,
    CategoryRoutingModule,
    DndModule,
    ReactiveFormsModule,
    LayoutModule,
    NgSelectModule
  ]
})
export class CategoryModule {
}
