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

import { Component, Input, OnDestroy, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { checkTypeExistsValidator, TypeService } from '../../../services/type.service';
import { CmdbMode } from '../../../modes.enum';
import { CategoryService } from '../../../services/category.service';
import { CmdbCategory } from '../../../models/cmdb-category';
import { Subscription } from 'rxjs';


@Component({
  selector: 'cmdb-type-basic-step',
  templateUrl: './type-basic-step.component.html',
  styleUrls: ['./type-basic-step.component.scss'],
})
export class TypeBasicStepComponent implements OnInit, OnDestroy {

  @Input()
  set preData(data: any) {
    if (data !== undefined) {
      this.basicForm.patchValue(data);
      this.basicMetaIconForm.patchValue(data.render_meta === undefined ? '' : data.render_meta);
    }
  }

  @Input() public mode: CmdbMode;
  public modes = CmdbMode;

  public basicForm: FormGroup;
  public basicMetaIconForm: FormGroup;

  public basicCategoryForm: FormGroup;
  private categoriesSubscription: Subscription;
  public categories: CmdbCategory[];

  constructor(private typeService: TypeService, private categoryService: CategoryService) {
    this.categoriesSubscription = new Subscription();
    this.basicForm = new FormGroup({
      name: new FormControl('', Validators.required),
      label: new FormControl('', Validators.required),
      description: new FormControl(''),
      active: new FormControl(true)
    });
    this.basicMetaIconForm = new FormGroup({
      icon: new FormControl(''),
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
    this.categoriesSubscription = this.categoryService.getCategoryList().subscribe((categories: CmdbCategory[]) => {
      this.categories = categories;
    });
    if (this.mode === CmdbMode.Create) {
      this.basicForm.get('name').setAsyncValidators(checkTypeExistsValidator(this.typeService));
      this.basicForm.get('label').valueChanges.subscribe(value => {
        this.basicForm.get('name').setValue(value.replace(/ /g, '-').toLowerCase());
        const newValue = this.basicForm.get('name').value;
        this.basicForm.get('name').setValue(newValue.replace(/[^a-z0-9 \-]/gi, '').toLowerCase());
        this.basicForm.get('name').markAsDirty({ onlySelf: true });
        this.basicForm.get('name').markAsTouched({ onlySelf: true });
      });
    } else if (this.mode === CmdbMode.Edit) {
      this.basicForm.markAllAsTouched();
    }
  }

  public ngOnDestroy(): void {
    this.categoriesSubscription.unsubscribe();
  }

}
