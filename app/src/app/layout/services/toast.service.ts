import { Injectable, TemplateRef } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class ToastService {

  toasts: any[] = [];

  show(textOrTpl: string | TemplateRef<any>, options: any = {}) {

    this.toasts.push({textOrTpl, ...options});

    console.log(this.toasts);
  }

  remove(toast) {
    this.toasts = this.toasts.filter(t => t !== toast);
  }
}
