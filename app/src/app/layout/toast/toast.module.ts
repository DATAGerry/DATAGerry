import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ToastContainerComponent } from './toast-container/toast-container.component';
import { NgbToastModule } from '@ng-bootstrap/ng-bootstrap';
import { ToastComponentComponent } from './toast-container/toast-component/toast-component.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

@NgModule({
  declarations: [ToastContainerComponent, ToastComponentComponent],
  imports: [
    CommonModule,
    NgbToastModule
  ],
  exports: [ToastContainerComponent]
})
export class ToastModule { }
