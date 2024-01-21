/*
* DATAGERRY - OpenSource Enterprise CMDB
* Copyright (C) 2024 becon GmbH
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


/**
 * Helper component to show a builder step validation status.
 */
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
  /**
   * Name of the step
   */
  @Input() public step: string = '';

  /**
   * Validation status of the step
   */
  @Input() public status: boolean = true;
}


/**
 * Abstract class for every builder step
 */
@Component({
  selector: 'cmdb-type-builder-step',
  template: ''
})
export class TypeBuilderStepComponent {

  /**
   * Render Modes
   */
  public modes = CmdbMode;

  /**
   * Selected render mode
   */
  @Input() public mode: CmdbMode = CmdbMode.View;

  /**
   * Type instance
   */
  @Input() public typeInstance: CmdbType;

  /**
   * List of all possible groups
   */
  @Input() public groups: Array<Group> = [];

  /**
   * List of all possible users
   */
  @Input() public users: Array<User> = [];

  /**
   * List of all possible categories
   */
  @Input() public categories: Array<CmdbCategory> = [];

  /**
   * List of possible types
   */
  @Input() public types: Array<CmdbType> = [];

  /**
   * Is the step valid
   */
  @Input() public valid: boolean = true;

  /**
   * Validation change emitter
   */
  @Output() public validateChange: EventEmitter<boolean> = new EventEmitter<boolean>();

  /**
   * Constructor of `TypeBuilderStepComponent`
   */
  public constructor() {
  }

}
