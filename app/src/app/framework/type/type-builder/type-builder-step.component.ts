/*
* DATAGERRY - OpenSource Enterprise CMDB
* Copyright (C) 2019 - 2021 NETHINKS GmbH
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
import { CmdbMode } from '../../modes.enum';
import { CmdbType } from '../../models/cmdb-type';
import { Group } from '../../../management/models/group';
import { User } from '../../../management/models/user';
import { CmdbCategory } from '../../models/cmdb-category';

@Component({
  selector: 'cmdb-type-builder-step-status',
  styles: [`span i {
    float: right;
    padding-top: 3px;
  }`, `.step-valid i {
    color: #28a745;
  }`, `.step-invalid i {
    color: #dc3545;
  }`],
  template: `{{step}}:
  <span *ngIf="status" class="step-valid">
    <i class="far fa-check-circle"></i>
  </span>
  <span *ngIf="!status" class="step-invalid">
    <i class="fas fa-exclamation-circle"></i>
  </span>
  <div class="clearfix"></div>
  `
})
export class TypeBuilderStepValidStatusComponent {
  @Input() public step: string = 'true';
  @Input() public status: boolean = true;
}


@Component({
  selector: 'cmdb-type-builder-step',
  template: ''
})
export class TypeBuilderStepComponent {

  public modes = CmdbMode;
  @Input() public mode: CmdbMode = CmdbMode.View;
  @Input() public typeInstance: CmdbType;

  @Input() public groups: Array<Group> = [];
  @Input() public users: Array<User> = [];
  @Input() public categories: Array<CmdbCategory> = [];

  @Input() public validate: boolean = true;
  @Output() public validateChange: EventEmitter<boolean> = new EventEmitter<boolean>();

  public constructor() {
  }

}
