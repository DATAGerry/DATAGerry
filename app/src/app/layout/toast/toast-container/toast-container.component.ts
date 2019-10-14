import { Component, HostBinding, TemplateRef } from '@angular/core';
import { ToastService } from '../toast.service';

@Component({
  selector: 'cmdb-toast-container',
  templateUrl: './toast-container.component.html',
  styleUrls: ['./toast-container.component.scss']
})
export class ToastContainerComponent {
  @HostBinding('class.ngb-toasts') toasts = true;

  constructor(public toastService: ToastService) {
  }

  isTemplate(toast) {
    return toast.textOrTpl instanceof TemplateRef;
  }
}
