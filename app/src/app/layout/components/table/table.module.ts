import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActionViewComponent } from './components/actions/action-view/action-view.component';
import { ActionEditComponent } from './components/actions/action-edit/action-edit.component';
import { ActionDeleteComponent } from './components/actions/action-delete/action-delete.component';
import { ActionsComponent } from './components/actions/actions.component';
import { RouterModule } from '@angular/router';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';

@NgModule({
  declarations: [
    ActionViewComponent,
    ActionEditComponent,
    ActionDeleteComponent,
    ActionsComponent
  ],
  exports: [
    ActionsComponent
  ],
  imports: [
    CommonModule,
    RouterModule,
    FontAwesomeModule
  ]
})
export class TableModule {
}
