/*
* DATAGERRY - OpenSource Enterprise CMDB
* Copyright (C) 2021 NETHINKS GmbH
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
* along with this program. If not, see <https://www.gnu.org/licenses/>.
*/

import {Directive, HostBinding, HostListener, Input} from '@angular/core';

export enum KEY_CODE {
  ENTER = 'Enter'
}

@Directive({
  // tslint:disable-next-line:directive-selector
  selector: 'button[type=submit]'
})
export class PreventDoubleSubmitDirective {

  @Input() valid: boolean = true;
  @HostBinding() disabled: boolean = false;

  @HostListener('click')
  onClick() {
    if (this.valid) { this.disabled = true; }
  }

  @HostListener('document:keypress', ['$event'])
  onEnter(event: KeyboardEvent | undefined) {
    if (event && KEY_CODE.ENTER === event.key && this.valid) { this.disabled = true; }
  }
}
