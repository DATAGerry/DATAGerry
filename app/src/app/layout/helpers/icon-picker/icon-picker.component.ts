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

// Fontawesome
import { FaIconLibrary } from '@fortawesome/angular-fontawesome';

export interface FontAwesomeIcon {
  [pack: string]: string;
}

@Component({
  selector: 'cmdb-icon-picker',
  templateUrl: './icon-picker.component.html',
  styleUrls: ['./icon-picker.component.scss']
})
export class IconPickerComponent {

  private preSelectedIcon: string = 'cube';
  public icons: FontAwesomeIcon[] = [];
  public packs: { [key: string]: string } = {fas: 'Solid', far: 'Regular', fab: 'Brands'};

  @Input() iconFormGroup: FormGroup;
  @Input() inputDescription: string = 'Symbol for the type label';

  @Input()
  public set fallbackIcon(value: string) {
    if (value != null) {
      if (value.includes('fas fa-')) {
        this.preSelectedIcon = value.replace('fas fa-', '');
      } else if (value.includes('far fa-')) {
        this.preSelectedIcon = value.replace('far fa-', '');
      } else if (value.includes('fab fa-')) {
        this.preSelectedIcon = value.replace('fab fa-', '');
      } else {
        this.preSelectedIcon = value;
      }
    } else {
      this.preSelectedIcon = 'cube';
    }
  }

  public get fallbackIcon(): string {
    return !this.preSelectedIcon ? 'cube' : this.preSelectedIcon;
  }

  constructor(private library: FaIconLibrary) {
    // @ts-ignore
    const fasArray = Object.keys(library.definitions.fas);
    // @ts-ignore
    const farArray = Object.keys(library.definitions.far);
    // @ts-ignore
    const fabArray = Object.keys(library.definitions.fab);

    fasArray.forEach(icon => this.icons.push({key: 'fas', name: icon}));
    farArray.forEach(icon => this.icons.push({key: 'far', name: icon}));
    fabArray.forEach(icon => this.icons.push({key: 'fab', name: icon}));
  }

  onIconPickerSelect(value: any = {key: 'fas', name: 'cube'}): void {
    const {key, name} = value;
    this.iconFormGroup.get('icon').setValue(`${key} fa-${name}`);
    this.fallbackIcon = name;
  }
}
