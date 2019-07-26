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

import { Component, OnInit } from '@angular/core';
import { CmdbCategory } from '../../models/cmdb-category';
import { CategoryService } from '../../services/category.service';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { TypeService } from '../../services/type.service';
import { CmdbType } from '../../models/cmdb-type';
import { ToastService } from '../../../layout/services/toast.service';

@Component({
  selector: 'cmdb-category-management',
  templateUrl: './category-management.component.html',
  styleUrls: ['./category-management.component.scss']
})
export class CategoryManagementComponent implements OnInit {

  public categoryList: CmdbCategory[];
  public typeList: CmdbType[];
  public categoryAddForm: FormGroup;
  public categoryEditForm: FormGroup;
  public selectedEditCategory: CmdbCategory;

  constructor(private categoryService: CategoryService, private typeService: TypeService, private toast: ToastService) {
    this.categoryAddForm = new FormGroup({
      name: new FormControl('', Validators.required),
      label: new FormControl('', Validators.required),
      parent_id: new FormControl(null),
      type_list: new FormControl(null)
    });

    this.categoryEditForm = new FormGroup({
      public_id: new FormControl(null),
      name: new FormControl('', Validators.required),
      label: new FormControl('', Validators.required),
      parent_id: new FormControl(null),
      type_list: new FormControl(null)
    });

  }

  public ngOnInit(): void {
    this.categoryService.getCategoryList().subscribe((list: CmdbCategory[]) => {
      this.categoryList = list;
    });
    this.typeService.getTypeList().subscribe((typeList: CmdbType[]) => {
      this.typeList = typeList;
    });
  }

  public addCategory(): void {
    const tmpCategory = new CmdbCategory();
    tmpCategory.name = this.categoryAddForm.get('name').value;
    tmpCategory.label = this.categoryAddForm.get('label').value;
    tmpCategory.parent_id = this.categoryAddForm.get('parent_id').value;
    tmpCategory.type_list = this.categoryAddForm.get('type_list').value;

    this.categoryService.postCategory(tmpCategory).subscribe(resp => {
        tmpCategory.public_id = +resp;
      }, (error) => {
        console.error(error);
      },
      () => {
        this.categoryList.push(tmpCategory);
      });
    this.categoryAddForm.reset();
  }

  public selectCategory(publicID: number): void {
    this.categoryEditForm.reset();
    this.selectedEditCategory = this.categoryList.find(category => category.public_id === publicID);
    this.categoryEditForm.patchValue(this.selectedEditCategory);
  }

  public editCategory(): void {
    this.categoryService.updateCategory(this.categoryEditForm.value).subscribe((resp: number) => {
      if (resp > 0) {
        this.toast.show('Category was updated');
      }
    }, (error) => {
      console.error(error);
    }, () => {
      this.categoryService.getCategoryList().subscribe((list: CmdbCategory[]) => {
        this.categoryList = list;
      });
    });
  }

}
