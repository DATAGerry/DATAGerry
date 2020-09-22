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

import {Injectable} from '@angular/core';

@Injectable({
  providedIn: 'root'
})

export class ToastService {

  public toastsright: any[] = [];
  public toastsleft: any[] = [];
  public toastsdownleft: any[] = [];
  public toastsdownright: any[] = [];
  public toastscenter: any[] = [];


  public showToast(text: string, options: any = {}, direction?: string) {
    if (!options.icon) {
      options.icon = 'fas fa-info-circle';
    }
    switch (direction) {
      case 'right': {
        this.toastsright.push({text, ...options});
        break;
      }
      case 'left': {
        this.toastsleft.push({text, ...options});
        break;
      }
      case 'downleft': {
        this.toastsdownleft.push({text, ...options});
        break;
      }
      case 'downright': {
        this.toastsdownright.push({text, ...options});
        break;
      }
      case 'center': {
        this.toastscenter.push({text, ...options});
        break;
      }
      default: {
        this.toastsright.push({text, ...options});
        break;
      }
    }
  }

  public error(text: string, options: any = {}, direction?: string) {
    options.classname += ' border-danger';
    options.headerName = 'An Error Occured';
    options.headerClass = 'text-danger';
    options.icon = 'fas fa-exclamation-circle';
    this.showToast(text, options, direction);
  }
  public warning(text: string, options: any = {}, direction?: string) {
    options.classname += ' border-warning';
    options.headerName = 'Warning';
    options.headerClass = 'text-warning';
    options.icon = 'fas fa-exclamation-triangle';
    this.showToast(text, options, direction);
  }

  public success(text: string, options: any = {}, direction?: string) {
    options.classname += ' border-success';
    options.headerName = 'Success';
    options.headerClass = 'text-success';
    options.icon = 'fas fa-check-circle';
    this.showToast(text, options, direction);
  }

  public info(text: string, options: any = {}, direction?: string) {
    options.classname += ' border-info';
    options.headerName = 'Information';
    options.headerClass = 'text-info';
    options.icon = 'fas fa-info-circle';
    this.showToast(text, options, direction);
  }


  public remove(toast) {
    this.toastscenter =  this.toastscenter.filter(t => t !== toast);
    this.toastsdownright =  this.toastsdownright.filter(t => t !== toast);
    this.toastsdownleft =  this.toastsdownleft.filter(t => t !== toast);
    this.toastsleft =  this.toastsleft.filter(t => t !== toast);
    this.toastsright =  this.toastsright.filter(t => t !== toast);
  }

}
