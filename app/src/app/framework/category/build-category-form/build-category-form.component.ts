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

import {Component, Input, OnInit} from '@angular/core';
import {CmdbCategory} from '../../models/cmdb-category';
import {CmdbType} from '../../models/cmdb-type';
import {FormControl, FormGroup, Validators} from '@angular/forms';
import {CategoryService} from '../../services/category.service';
import {TypeService} from '../../services/type.service';
import {ToastService} from '../../../layout/services/toast.service';
import {NgbModal} from '@ng-bootstrap/ng-bootstrap';
import {DndDropEvent, DropEffect} from 'ngx-drag-drop';
import {ActivatedRoute, Router} from '@angular/router';
import {CmdbMode} from '../../modes.enum';

@Component({
  selector: 'cmdb-build-category-form',
  templateUrl: './build-category-form.component.html',
  styleUrls: ['./build-category-form.component.scss']
})
export class BuildCategoryFormComponent implements OnInit {

  @Input() categoryForm: FormGroup;
  @Input() mode: CmdbMode = CmdbMode.Create;
  public category: CmdbCategory;
  public categoryList: CmdbCategory[];
  public categoryID: number;
  public typeList: CmdbType[];
  public parentCategories: CmdbCategory[] = [];
  public assignedTypes: CmdbType[] = [];
  public filterCategories: string = '';
  public filterTypes: string = '';
  private toUpdateTypes: CmdbType[] = [];

  constructor(private categoryService: CategoryService, private typeService: TypeService, private router: Router,
              private toast: ToastService, private modalService: NgbModal, private activateRoute: ActivatedRoute) {

    this.activateRoute.params.subscribe(params => {
      this.categoryID = params.publicID;
    });

    this.categoryForm = new FormGroup({
      name: new FormControl('', Validators.required),
      label: new FormControl('', Validators.required),
    });
  }

  ngOnInit() {
    if (this.categoryID !== undefined) {
      this.categoryService.getCategory(this.categoryID).subscribe(value => {
        this.category = value;
      }, error => { console.log(error); },
      () => {
        this.categoryForm.get('label').setValue(this.category.label);
        this.categoryForm.get('name').setValue(this.category.name);
        this.typeService.getTypeListByCategory(this.categoryID).subscribe((typeList: CmdbType[]) => {
          this.assignedTypes = typeList;
          this.toUpdateTypes = typeList;
        });
        if (this.category.parent_id !== 0) {
          this.categoryService.getCategory(this.category.parent_id).subscribe((value: CmdbCategory) => {
            this.parentCategories.push(value);
          });
        }
      });
    }

    this.categoryService.getCategoryList().subscribe((list: CmdbCategory[]) => {
      this.categoryList = list;
      if (this.categoryID !== undefined && this.category !== undefined) {
        list = list.filter(item => item.public_id !== this.category.public_id);
        this.categoryList = list.filter(item => item.public_id !== this.category.parent_id);
      }
    });

    this.typeService.getTypeListByCategory(0).subscribe((typeList: CmdbType[]) => {
      this.typeList = typeList;
    });

    if (this.mode === CmdbMode.Create) {
      this.categoryForm.get('label').valueChanges.subscribe(value => {
        value = value == null ? '' : value;
        this.categoryForm.get('name').setValue(value.replace(/ /g, '-').toLowerCase());
        this.categoryForm.get('name').markAsDirty({onlySelf: true});
        this.categoryForm.get('name').markAsTouched({onlySelf: true});
      });
    }

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

    if (this.toUpdateTypes.length !== 0) {
      const tempType = this.toUpdateTypes.find(value => value.public_id === item.data.public_id);
      if (tempType !== undefined) {
        tempType.category_id = this.category.public_id;
      }
    } else {
      this.toUpdateTypes.push(item.data);
      item.data.category_id = this.category.public_id;
    }
  }

  public removeAssignedType(item: CmdbType): void {
    this.typeList.push(item);
    this.assignedTypes = this.assignedTypes.filter(value => value.public_id !== item.public_id);

    if (this.toUpdateTypes.length !== 0) {
      const tempType = this.toUpdateTypes.find(value => value.public_id === item.public_id);
      if (tempType !== undefined) {
        tempType.category_id = 0;
      }
    }
  }

  public onSubmit(): void {
    const tmpCategory: CmdbCategory = this.mode === CmdbMode.Create ? new CmdbCategory() : this.category;
    tmpCategory.name = this.categoryForm.get('name').value;
    tmpCategory.label = this.categoryForm.get('label').value;
    tmpCategory.parent_id = this.parentCategories.length > 0 ? this.parentCategories.pop().public_id : 0;

    if (this.mode === CmdbMode.Create) {
      this.addCategory(tmpCategory);
    } else if (this.mode === CmdbMode.Edit) {
      this.editCategory(tmpCategory);
    }
  }

  public addCategory(tmpCategory: CmdbCategory): void {
    this.categoryService.postCategory(tmpCategory).subscribe(resp => {
      tmpCategory.public_id = +resp;
    }, (error) => {
      console.error(error);
    },
    () => {
      this.reloadData('Category was created');
    });
    this.categoryForm.reset();
  }

  public editCategory(tmpCategory: CmdbCategory): void {
    this.categoryService.updateCategory(tmpCategory).subscribe((resp: number) => {
      console.log(resp);
    }, (error) => {
      console.error(error);
    }, () => {
      this.reloadData('Category was updated');
    });
  }

  private reloadData(toastMessage: string) {
    this.categoryService.getCategoryList().subscribe((list: CmdbCategory[]) => {
      this.categoryList = list;
    }, (error) => {
      console.log(error);
    }, () => {
      for (const type of this.toUpdateTypes) {
        this.typeService.putType(type).subscribe((updateResp: CmdbType) => {
          console.log('');
        });
      }
      this.toast.show(toastMessage);
      this.router.navigate(['/framework/category/']);
    });
  }
}
