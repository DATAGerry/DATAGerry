/*
* DATAGERRY - OpenSource Enterprise CMDB
* Copyright (C) 2019 - 2020 NETHINKS GmbH
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

@Component({
  selector: 'cmdb-local-authentication-provider-form',
  templateUrl: './local-authentication-provider-form.component.html',
  styleUrls: ['./local-authentication-provider-form.component.scss']
})
export class LocalAuthenticationProviderFormComponent {

  public form: FormGroup;

  public parent: FormArray;
  public provider: AuthProvider;

  @Input('parent')
  public set Parent(form: FormArray) {
    this.parent = form;
    this.parent.insert(0, new FormGroup({
      class_name: new FormControl('LocalAuthenticationProvider'),
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
      active: new FormControl()
    });
    this.form.get('active').disable({onlySelf: true});
  }

}
