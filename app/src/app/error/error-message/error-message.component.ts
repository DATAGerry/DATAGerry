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

import { Component, EventEmitter, Input, Output, ViewEncapsulation } from '@angular/core';
import { BackendHttpError } from '../models/custom.error';

@Component({
  selector: 'cmdb-error-message',
  templateUrl: './error-message.component.html',
  styleUrls: ['./error-message.component.scss'],
  encapsulation: ViewEncapsulation.None,
  // tslint:disable-next-line:no-host-metadata-property
  host: {
    role: 'alert',
    '[attr.aria-live]': 'ariaLive',
    'aria-atomic': 'true',
    '[class.toast]': 'true',
    '[class.show]': 'true',
  },
})
export class ErrorMessageComponent {

  @Input() public error: BackendHttpError = undefined;
  @Output() public hideOut = new EventEmitter<void>();

  public onHide() {
    this.hideOut.emit();
  }

}
