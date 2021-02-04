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

  /**
   * The configuration form for the ldap auth provider.
   */
  public form: FormGroup;

  /**
   * The parent holder of the auth settings provider array.
   */
  public parent: FormArray;

  /**
   * Auth provider type.
   */
  public provider: AuthProvider;

  /**
   * List of a possible mapping groups.
   */
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
    if (provider) {
      provider.config.groups.mapping.forEach((value, index) => {
        const formGroup = new FormGroup({
          group_dn: new FormControl(value.group_dn),
          group_id: new FormControl(value.group_id)
        });
        this.groupMappingControl.insert(index, formGroup);
      });

    }
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
      groups: new FormGroup({
        active: new FormControl(false),
        searchfiltergroup: new FormControl(),
        mapping: new FormArray([])
      })
    });
  }

  /**
   * Ldap server config control.
   */
  public get serverConfigControl(): FormGroup {
    return this.form.get('server_config') as FormGroup;
  }

  /**
   * Ldap connection config control.
   */
  public get connectionConfigControl(): FormGroup {
    return this.form.get('connection_config') as FormGroup;
  }

  /**
   * Ldap user search control.
   */
  public get searchControl(): FormGroup {
    return this.form.get('search') as FormGroup;
  }

  /**
   * Ldap groups control.
   */
  public get groupsControl(): FormGroup {
    return this.form.get('groups') as FormGroup;
  }

  /**
   * Nested ldap groups mapping form array.
   */
  public get groupMappingControl(): FormArray {
    return this.groupsControl.get('mapping') as FormArray;
  }

}
