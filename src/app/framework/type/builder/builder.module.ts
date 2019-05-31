import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { BuilderComponent } from './builder.component';
import { DndModule } from 'ngx-drag-drop';
import { RenderModule } from '../../render/render.module';
import { FormsModule } from '@angular/forms';
import { NgSelectModule } from '@ng-select/ng-select';

@NgModule({
  declarations: [
    BuilderComponent
  ],
  imports: [
    CommonModule,
    DndModule,
    RenderModule,
    FormsModule,
    NgSelectModule
  ],
  exports: [
    BuilderComponent
  ]
})
export class BuilderModule { }
