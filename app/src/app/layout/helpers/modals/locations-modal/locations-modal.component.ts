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
* along with this program.  If not, see <https://www.gnu.org/licenses/>.
*/

import {Component, Input } from '@angular/core';
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';
/* -------------------------------------------------------------------------- */


@Component({
  selector: 'cmdb-locations-modal',
  templateUrl: './locations-modal.component.html',
  styleUrls: ['./locations-modal.component.scss']
})
export class LocationsModalComponent {
  @Input() title = 'Information';
  @Input() modalIcon = 'trash';
  @Input() modalMessage = `This object has a location which is a parent to other locations and can't be deleted alone. 
                           If you want to delete this object and all children objects with their locations press 'Objects and Locations'.
                           If you want to delete only the locations of the child objects press 'Locations'.`;
  @Input() subModalMessage = '';
  @Input() deleteObjectsButton = 'Objects and Locations';
  @Input() deleteChildrenButton = 'Locations';
  @Input() cancelButton = 'Cancel';

  constructor(public activeModal: NgbActiveModal) {}
}