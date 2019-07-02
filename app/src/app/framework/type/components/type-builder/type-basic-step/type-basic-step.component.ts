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
import { AbstractControl, FormControl, FormGroup, Validators } from '@angular/forms';
import { TypeService } from '../../../../services/type.service';
import { CategoryService } from '../../../../services/category.service';
import { CmdbCategory } from '../../../../models/cmdb-category';
import { Observable } from 'rxjs';
import { Modes } from '../../../builder/modes.enum';


@Injectable()
export class TypeNameValidator {

  static createValidator(typeService: TypeService, mode: number) {
    return (control: AbstractControl) => {
      return typeService.validateTypeName(control.value).then(res => {
        if (mode === Modes.Edit) {
          return null;
        }
        return res ? null : {nameAlreadyTaken: true};
      });
    };
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

  @Input() mode: number;

  public basicForm: FormGroup;
  public basicCategoryForm: FormGroup;
  private categoryList: Observable<CmdbCategory[]>;

  constructor(private typeService: TypeService, private categoryService: CategoryService) {
    this.basicForm = new FormGroup({
      name: new FormControl('', [Validators.required], TypeNameValidator.createValidator(typeService, this.mode)),
      label: new FormControl('', Validators.required),
      description: new FormControl(''),
      active: new FormControl(true)
    });
    this.basicCategoryForm = new FormGroup({
      category_id: new FormControl(null)
    });
  }

  public get name() {
    return this.basicForm.get('name');
  }

  public get label() {
    return this.basicForm.get('label');
  }

  public ngOnInit(): void {
    this.categoryList = this.categoryService.getCategoryList();
    this.basicForm.get('name').valueChanges.subscribe(val => {
      this.basicForm.get('label').setValue(val.toString().charAt(0).toUpperCase() + val.toString().slice(1));
      this.basicForm.get('label').markAsDirty({onlySelf: true});
      this.basicForm.get('label').markAsTouched({onlySelf: true});
    });
  }


}
