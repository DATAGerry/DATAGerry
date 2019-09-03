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

import { Component, Input } from '@angular/core';
import { FormGroup } from '@angular/forms';

@Component({
  selector: 'cmdb-icon-picker',
  templateUrl: './icon-picker.component.html',
  styleUrls: ['./icon-picker.component.scss']
})
export class IconPickerComponent {

  @Input() iconFormGroup: FormGroup;
  @Input() inputDescription: string = 'Symbol for the type label';
  @Input() preSelectedIcon: string;
  public fallBackIcon: string;

  @Input()
  public set fallbackIcon(value: string) {
    this.fallBackIcon = value;
  }

  public get fallbackIcon(): string {
    if (this.fallBackIcon === undefined || this.fallBackIcon === '') {
      return 'fa fa-cube';
    }
    return this.fallBackIcon;
  }

  onIconPickerSelect(value: string): void {
    this.iconFormGroup.get('icon').setValue(value);
  }
}
