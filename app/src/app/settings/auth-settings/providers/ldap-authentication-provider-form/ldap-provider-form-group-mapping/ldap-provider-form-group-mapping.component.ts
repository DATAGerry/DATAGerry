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

import { Component, Input } from '@angular/core';
import { Group } from '../../../../../management/models/group';
import { FormArray, FormControl, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'cmdb-ldap-provider-form-group-mapping',
  templateUrl: './ldap-provider-form-group-mapping.component.html',
  styleUrls: ['./ldap-provider-form-group-mapping.component.scss']
})
export class LdapProviderFormGroupMappingComponent {

  @Input() public groups: Array<Group> = [];
  @Input() public mappingFormArray: FormArray = new FormArray([]);

  public form: FormGroup;

  constructor() {
    this.form = new FormGroup({
      group_dn: new FormControl('', Validators.required),
      group_id: new FormControl(null, Validators.required)
    });
  }

  public get groupDNValue(): string {
    return this.form.get('group_dn').value;
  }

  public get groupIDValue(): number {
    return +this.form.get('group_id').value;
  }

  public addMapping(): void {
    if (this.form.valid) {
      const mappingFormGroup = new FormGroup({
        group_dn: new FormControl(this.groupDNValue),
        group_id: new FormControl(this.groupIDValue)
      });
      this.mappingFormArray.insert(this.mappingFormArray.controls.length, mappingFormGroup);
    }
  }

}
