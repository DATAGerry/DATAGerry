/*
* DATAGERRY - OpenSource Enterprise CMDB
* Copyright (C) 2023 becon GmbH
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
*
* You should have received a copy of the GNU Affero General Public License
* along with this program. If not, see <https://www.gnu.org/licenses/>.
*/

import { Component, EventEmitter, Input, Output } from '@angular/core';
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';

@Component({
  selector: 'cmdb-object-delete-modal',
  templateUrl: './object-delete-modal.component.html',
  styleUrls: ['./object-delete-modal.component.scss']
})
export class ObjectDeleteModalComponent {

  @Input() public publicID: number = null;
  @Output() public closeEmitter: EventEmitter<number> = new EventEmitter<number>();

  constructor(public activeModal: NgbActiveModal) {
  }
}
