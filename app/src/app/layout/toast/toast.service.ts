/*
* DATAGERRY - OpenSource Enterprise CMDB
* Copyright (C) 2019 NETHINKS GmbH
*
* This program is free software: you can redistribute it and/or modify
* it under the terms of the GNU Affero General Public License as
* published by the Free Software Foundation, either version 3 of the
* License, or (at your option) any later version.
*
* This program is distributed in the hope that it will be useful,
* but WITHOUT ANY WARRANTY; without even the implied warranty of
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
* GNU Affero General Public License for more details.

* You should have received a copy of the GNU Affero General Public License
* along with this program.  If not, see <https://www.gnu.org/licenses/>.
*/

import {EventEmitter, Injectable, Output, TemplateRef} from '@angular/core';
import './toast.js';

declare global {
  interface Window {
    showToast(): void;
  }
}

@Injectable({
  providedIn: 'root'
})

export class ToastService {

  @Output() toast: EventEmitter<any> = new EventEmitter();

  toasts: any[] = [];
  errorToast: any[] = [];

  // public info(textOrTpl: string | TemplateRef<any>, options: any = {}) {
  //   options.classname += ' bg-info';
  //   options.headerName = 'Information';
  //   options.headerClass = 'text-info';
  //   this.toasts.push({ textOrTpl, ...options });
  // }

  public info(text: string, options: any = {}) {
    this.toast.emit();
    window.showToast();
    // // $('#info').toast('show');
    // this.toasts.push({text, ...options});
  }

  // public error(textOrTpl: string | TemplateRef<any>, options: any = {}) {
  //   options.classname += ' bg-danger';
  //   this.errorToast.push({ textOrTpl, ...options });
  // }
  //
  // public warning(textOrTpl: string | TemplateRef<any>, options: any = {}) {
  //   options.classname += ' bg-warning';
  //   options.headerName = 'Warning';
  //   options.headerClass = 'text-warning';
  //   this.toasts.push({ textOrTpl, ...options });
  // }
  //
  // public success(textOrTpl: string | TemplateRef<any>, options: any = {}) {
  //   options.classname += ' bg-success';
  //   options.headerName = 'Success';
  //   options.headerClass = 'text-success';
  //   this.toasts.push({ textOrTpl, ...options });
  // }
  //
  // public remove(toast) {
  //   this.toasts = this.toasts.filter(t => t !== toast);
  // }
  //
  // public removeError(toast) {
  //   this.errorToast = this.errorToast.filter(t => t !== toast);
  // }
}
