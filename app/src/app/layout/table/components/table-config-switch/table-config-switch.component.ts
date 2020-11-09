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
import { TableConfig } from '../../table.types';

@Component({
  // tslint:disable-next-line:component-selector
  selector: 'table-config-switch',
  templateUrl: './table-config-switch.component.html',
  styleUrls: ['./table-config-switch.component.scss']
})
export class TableConfigSwitchComponent implements OnInit {

  @Input() public tableConfigs: Array<TableConfig> = [];

  @Input() public tableConfig: TableConfig;

  @Output() public configSelect: EventEmitter<TableConfig> = new EventEmitter<TableConfig>();
  @Output() public configSave: EventEmitter<TableConfig> = new EventEmitter<TableConfig>();
  @Output() public configDelete: EventEmitter<TableConfig> = new EventEmitter<TableConfig>();
  @Output() public configReset: EventEmitter<void> = new EventEmitter<void>();

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

  public selectConfig(config: TableConfig) {
    this.configSelect.emit(config);
  }

  public resetConfig() {
    this.configReset.emit();
  }

  public saveConfig(name?: string) {
    const saveTableConfig: TableConfig = Object.assign({}, this.tableConfig) as TableConfig;
    saveTableConfig.name = name;
    this.configSave.emit(saveTableConfig);
    this.nameControl.setValue('');
  }

  public deleteConfig(config: TableConfig) {
    const index = this.tableConfigs.indexOf(config, 0);
    if (index > -1) {
      this.tableConfigs.splice(index, 1);
    }
    this.configDelete.emit(config);
  }

}
