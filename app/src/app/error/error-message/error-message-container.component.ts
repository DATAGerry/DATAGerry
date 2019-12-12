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

import { Component, HostBinding, OnInit } from '@angular/core';
import { BackendHttpError } from '../models/custom.error';
import { ErrorMessageService } from '../services/error-message.service';

@Component({
  // tslint:disable-next-line:component-selector
  selector: 'error-message-container',
  templateUrl: './error-message-container.component.html',
  styleUrls: ['./error-message-container.component.scss']
})
export class ErrorMessageContainerComponent implements OnInit {

  @HostBinding('class.error-message-container') class = 'error-message-container';
  public errorMessages: BackendHttpError[] = [];

  constructor(private errorService: ErrorMessageService) {

  }

  public ngOnInit(): void {
    this.errorService.getError().subscribe((error: BackendHttpError) => {
      const errorIndex = this.errorMessages.indexOf(error);
      if (errorIndex === -1) {
        this.errorMessages.push(error);
      } else {
        this.errorMessages = this.errorMessages.filter(t => t !== error);
      }
    });
  }

  public onHide(error: BackendHttpError) {
    this.errorService.remove(error);
  }

}
