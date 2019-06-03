/*
* dataGerry - OpenSource Enterprise CMDB
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

import { Component, Injectable, Input, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { TypeService } from '../../../../services/type.service';

@Injectable()
export class TypeNameValidator {

  constructor(private typeService: TypeService) {
  }

  checkName(control: FormControl): any {
    return this.typeService.validateTypeName(control.value);
  }
}

@Component({
  selector: 'cmdb-type-basic-step',
  templateUrl: './type-basic-step.component.html',
  styleUrls: ['./type-basic-step.component.scss'],
  providers: [TypeNameValidator]
})
export class TypeBasicStepComponent implements OnInit {

  @Input()
  set preData(data: any) {
    if (data !== undefined) {
      this.basicForm.patchValue(data);
    }
  }

  public basicForm: FormGroup;

  constructor(private typeNameValidator: TypeNameValidator) {

    this.basicForm = new FormGroup({
      name: new FormControl('', Validators.required, this.typeNameValidator.checkName.bind(this.typeNameValidator)),
      label: new FormControl('', Validators.required),
      description: new FormControl(''),
      active: new FormControl(true),
    });
  }

  public ngOnInit(): void {
    this.basicForm.get('name').valueChanges.subscribe(val => {
      this.basicForm.get('label').setValue(val.toString().charAt(0).toUpperCase() + val.toString().slice(1));

    });
  }


}
