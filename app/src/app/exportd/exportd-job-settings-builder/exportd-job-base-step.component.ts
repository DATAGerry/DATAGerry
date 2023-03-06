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

* You should have received a copy of the GNU Affero General Public License
* along with this program. If not, see <https://www.gnu.org/licenses/>.
*/

import { Component, EventEmitter, Input, Output } from '@angular/core';
import { CmdbType } from '../../framework/models/cmdb-type';
import { CmdbMode } from '../../framework/modes.enum';

@Component({
  selector: 'cmdb-exportd-job-base-step',
  template: '',
})
export class ExportdJobBaseStepComponent {

  public modes = CmdbMode;
  @Input() public mode: number = CmdbMode.Create;
  @Input() public types: Array<CmdbType> = [];
  @Input() public totalTypes: number = 0;
  @Output() public typeCallEmitter: EventEmitter<void> = new EventEmitter<void>();

  constructor() {
  }

}
