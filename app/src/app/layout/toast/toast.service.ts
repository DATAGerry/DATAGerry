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

import {EventEmitter, HostBinding, Injectable, Output, TemplateRef} from '@angular/core';

declare global {
  interface Window {
    showToast(): void;
  }
}

@Injectable({
  providedIn: 'root'
})

export class ToastService {

  toasts: any[] = [];
  errorToast: any[] = [];
  idGen: number = 0;

  // public info(textOrTpl: string | TemplateRef<any>, options: any = {}) {
  //   this.toasts.push({ textOrTpl, ...options });
  // }

  public incrementId(): void {
    this.idGen += 1;
  }

  public info(text: string, options: any = {}, animationDelay: number = 10) {
    this.incrementId();
    options.icon = 'fas fa-info-circle';
    options.classname += ' border-info';
    options.headerName = 'Information';
    options.headerClass = 'text-info';
    options.id = this.idGen.toString();
    options.delayTime = animationDelay;
    this.toasts.push({ text, ...options});
  }

  public error(text: string, options: any = {}, animationDelay: number = 7) {
    this.incrementId();
    options.icon = 'fas fa-exclamation-circle';
    options.classname += ' border-danger';
    options.headerName = 'An Error Occured';
    options.headerClass = 'text-danger';
    options.id = this.idGen.toString();
    options.delayTime = animationDelay;
    this.toasts.push({ text, ...options });
  }

  public warning(text: string, options: any = {}, animationDelay: number = 15) {
    this.incrementId();
    options.icon = 'fas fa-exclamation-triangle';
    options.classname += ' border-warning';
    options.headerName = 'Warning';
    options.headerClass = 'text-warning';
    options.id = this.idGen.toString();
    options.delayTime = animationDelay;
    this.toasts.push({ text, ...options });
  }

  public success(text: string, options: any = {}, animationDelay: number = 5) {
    this.incrementId();
    options.icon = 'fas fa-check-circle';
    options.classname += ' border-success';
    options.headerName = 'Success';
    options.headerClass = 'text-success';
    options.id = this.idGen.toString();
    options.delayTime = animationDelay;
    this.toasts.push({ text, ...options });
  }

  public remove(toast) {
    this.toasts = this.toasts.filter(t => t !== toast);
  }

  public removeError(toast) {
    this.errorToast = this.errorToast.filter(t => t !== toast);
  }
}
