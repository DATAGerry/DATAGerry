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

import { Component, OnInit } from '@angular/core';
import { CmdbCategory } from '../../models/cmdb-category';
import { CmdbType } from '../../models/cmdb-type';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { CategoryService } from '../../services/category.service';
import { TypeService } from '../../services/type.service';
import { ToastService } from '../../../layout/services/toast.service';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { DndDropEvent, DropEffect } from 'ngx-drag-drop';

@Component({
  selector: 'cmdb-category-add',
  templateUrl: './category-add.component.html',
  styleUrls: ['./category-add.component.scss']
})
export class CategoryAddComponent implements OnInit {

  public categoryList: CmdbCategory[];
  public typeList: CmdbType[];
  public categoryAddForm: FormGroup;
  public parentCategories: CmdbCategory[];
  public assignedTypes: CmdbType[];
  public filterCategories: string = '';
  public filterTypes: string = '';

  constructor(private categoryService: CategoryService, private typeService: TypeService,
              private toast: ToastService, private modalService: NgbModal) {
    this.categoryAddForm = new FormGroup({
      name: new FormControl('', Validators.required),
      label: new FormControl('', Validators.required),
    });
  }

  ngOnInit() {
    this.categoryService.getCategoryList().subscribe((list: CmdbCategory[]) => {
      this.categoryList = list;
    });
    this.typeService.getTypeList().subscribe((typeList: CmdbType[]) => {
      this.typeList = typeList;
    });
    this.parentCategories = [];
    this.assignedTypes = [];

    this.categoryAddForm.get('label').valueChanges.subscribe(value => {
      value = value == null ? '' : value;
      this.categoryAddForm.get('name').setValue(value.replace(/ /g, '-').toLowerCase());
      this.categoryAddForm.get('name').markAsDirty({onlySelf: true});
      this.categoryAddForm.get('name').markAsTouched({onlySelf: true});
    });

    const parent: any = document.getElementsByClassName('category-form')[0];
    const first: any = document.getElementsByClassName('drag-items')[0];
    const second: any = document.getElementsByClassName('drag-items')[1];
    first.style.height = parent.offsetHeight / 2 + 'px';
    second.style.height = parent.offsetHeight / 2 + 'px';
  }

  public onDraggedParent(item: DndDropEvent, list: any[], effect: DropEffect) {
    if (list.length !== 0) {
      this.categoryList.push(list.pop());
    }

    list.push(item.data);
    this.categoryList = this.categoryList.filter(category => category.public_id !== item.data.public_id);
  }

  public removeParent(item: CmdbCategory): void {
    this.parentCategories.length = 0;
    this.categoryList.push(item);
  }

  public onDraggedAssignedTypes(item: DndDropEvent, list: any[], effect: DropEffect) {
    list.push(item.data);
    this.typeList = this.typeList.filter(value => value.public_id !== item.data.public_id);
  }

  public removeAssignedType(item: CmdbType): void {
    this.typeList.push(item);
    this.assignedTypes = this.assignedTypes.filter(value => value.public_id !== item.public_id);
  }

  public addCategory(): void {
    const tmpCategory: CmdbCategory = new CmdbCategory();
    tmpCategory.name = this.categoryAddForm.get('name').value;
    tmpCategory.label = this.categoryAddForm.get('label').value;

    while (this.parentCategories.length > 0) {
      tmpCategory.parent_id = this.parentCategories.pop().public_id;
    }
    /*while (this.assignedTypes.length > 0) {
      tmpCategory.type_list.push(this.assignedTypes.pop().public_id);
    }*/

    this.categoryService.postCategory(tmpCategory).subscribe(resp => {
        tmpCategory.public_id = +resp;
      }, (error) => {
        console.error(error);
      },
      () => {
        this.categoryService.getCategoryList().subscribe((list: CmdbCategory[]) => {
          this.categoryList = list;
        });
      });
    this.categoryAddForm.reset();
  }
}
