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
import { AuthProvider } from '../../../../auth/models/providers';
import { FormArray, FormControl, FormGroup } from '@angular/forms';
import { Group } from '../../../../management/models/group';

@Component({
  selector: 'cmdb-ldap-authentication-provider-form',
  templateUrl: './ldap-authentication-provider-form.component.html',
  styleUrls: ['./ldap-authentication-provider-form.component.scss']
})
export class LdapAuthenticationProviderFormComponent {

  public form: FormGroup;
  public parent: FormArray;
  public provider: AuthProvider;

  @Input() public groups: Array<Group> = [];

  @Input('parent')
  public set Parent(form: FormArray) {
    this.parent = form;
    this.parent.insert(1, new FormGroup({
      class_name: new FormControl('LdapAuthenticationProvider'),
      config: this.form
    }));
  }

  @Input('provider')
  public set Provider(provider: AuthProvider) {
    this.provider = provider;
    this.form.patchValue(provider.config);
  }

  constructor() {
    this.form = new FormGroup({
      active: new FormControl(false),
      default_group: new FormControl(null),
      server_config: new FormGroup({
        host: new FormControl(),
        port: new FormControl(null),
        use_ssl: new FormControl(false)
      }),
      connection_config: new FormGroup({
        user: new FormControl(),
        password: new FormControl(),
        version: new FormControl(null)
      }),
      search: new FormGroup({
        basedn: new FormControl(),
        searchfilter: new FormControl()
      }),
      group_mapping: new FormGroup({
        active: new FormControl(false),
        searchfiltergroup: new FormControl(),
        mapping: new FormArray([])
      })
    });
  }

  public get serverConfigControl(): FormGroup {
    return this.form.get('server_config') as FormGroup;
  }

  public get connectionConfigControl(): FormGroup {
    return this.form.get('connection_config') as FormGroup;
  }

  public get searchControl(): FormGroup {
    return this.form.get('search') as FormGroup;
  }

  public get groupMappingControl(): FormGroup {
    return this.form.get('group_mapping') as FormGroup;
  }

  public get groupMappingMappingControl(): FormArray {
    return this.groupMappingControl.get('mapping') as FormArray;
  }

}
