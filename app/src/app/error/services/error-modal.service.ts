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

import { Injectable } from '@angular/core';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { ErrorModalComponent } from '../modals/error-modal.component';

@Injectable({
  providedIn: 'root'
})
export class ErrorModalService {
  public errors: any[];

  public constructor(private modalService: NgbModal) {
    this.errors = [];
  }

  public show(error: any): void {
    const modalRef = this.modalService.open(ErrorModalComponent);
    this.errors.push(error);
  }

  public remove(error: any): void {
    this.errors = this.errors.filter(err => err !== error);
  }

}
