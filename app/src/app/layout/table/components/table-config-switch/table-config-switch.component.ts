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
import { TableConfigUserSetting } from '../../table.types';

@Component({
  // tslint:disable-next-line:component-selector
  selector: 'table-config-switch',
  templateUrl: './table-config-switch.component.html',
  styleUrls: ['./table-config-switch.component.scss']
})
export class TableConfigSwitchComponent implements OnInit {

  @Input() public tableConfigs: Array<TableConfigUserSetting> = [];
  @Input() public currentConfig: TableConfigUserSetting;

  @Output() public configSelect: EventEmitter<TableConfigUserSetting> = new EventEmitter<TableConfigUserSetting>();
  @Output() public configSave: EventEmitter<TableConfigUserSetting> = new EventEmitter<TableConfigUserSetting>();
  @Output() public configDelete: EventEmitter<TableConfigUserSetting> = new EventEmitter<TableConfigUserSetting>();
  @Output() public configReset: EventEmitter<void> = new EventEmitter<void>();

  public form: FormGroup;

  constructor() {
    this.form = new FormGroup({
      label: new FormControl('', Validators.required)
    });
  }

  public ngOnInit(): void {
  }

  /**
   * Get the label control of the settings.
   */
  public get labelControl(): FormControl {
    return this.form.get('label') as FormControl;
  }

  public selectConfig(config: TableConfigUserSetting) {
    for (const conf of this.tableConfigs) {
      conf.active = conf === config;
    }
    this.configSelect.emit(config);
  }

  public resetConfig() {
    this.configReset.emit();
  }

  public saveConfig(label?: string) {
    const saveTableConfig: TableConfigUserSetting = Object.assign({}, this.currentConfig) as TableConfigUserSetting;
    saveTableConfig.label = label;
    this.configSave.emit(saveTableConfig);
    this.labelControl.setValue('');
  }

  public deleteConfig(config: TableConfigUserSetting) {
    const index = this.tableConfigs.indexOf(config, 0);
    if (index > -1) {
      this.tableConfigs.splice(index, 1);
    }
    this.configDelete.emit(config);
  }

}
