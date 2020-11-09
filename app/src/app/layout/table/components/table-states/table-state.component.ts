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
* along with this program. If not, see <https://www.gnu.org/licenses/>.
*/

import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { TableState } from '../../table.types';

@Component({
  // tslint:disable-next-line:component-selector
  selector: 'table-state',
  templateUrl: './table-state.component.html',
  styleUrls: ['./table-state.component.scss']
})
export class TableStateComponent implements OnInit {

  /**
   * Current possible table states
   */
  @Input() public tableStates: Array<TableState> = [];

  /**
   * Current selected state.
   */
  @Input() public currentState: TableState;

  @Output() public stateSelect: EventEmitter<TableState> = new EventEmitter<TableState>();
  @Output() public stateSave: EventEmitter<string> = new EventEmitter<string>();
  @Output() public stateDelete: EventEmitter<TableState> = new EventEmitter<TableState>();
  @Output() public stateReset: EventEmitter<void> = new EventEmitter<void>();

  public form: FormGroup;

  constructor() {
    this.form = new FormGroup({
      name: new FormControl('', Validators.required)
    });
  }

  public ngOnInit(): void {
  }

  /**
   * Get the control of the settings.
   */
  public get nameControl(): FormControl {
    return this.form.get('name') as FormControl;
  }

  public selectState(state: TableState) {
    this.stateSelect.emit(state);
  }

  public resetState() {
    this.stateReset.emit();
  }

  public saveState(name?: string) {
    this.stateSave.emit(name);
    this.nameControl.setValue('');
  }

  public deleteState(config: TableState) {
    const index = this.tableStates.indexOf(config, 0);
    if (index > -1) {
      this.tableStates.splice(index, 1);
    }
    this.stateDelete.emit(config);
  }

}
