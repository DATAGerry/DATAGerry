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

import { Component, Input, OnInit, AfterContentInit } from '@angular/core';
import { CmdbCategory } from '../../models/cmdb-category';
import { CmdbType } from '../../models/cmdb-type';
import { FormGroup } from '@angular/forms';
import { CategoryService, checkCategoryExistsValidator } from '../../services/category.service';
import { TypeService } from '../../services/type.service';
import { ToastService } from '../../../layout/toast/toast.service';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { DndDropEvent, DropEffect } from 'ngx-drag-drop';
import { ActivatedRoute, Router } from '@angular/router';
import { CategoryMode } from '../../modes.enum';
import { NgxSpinnerService } from 'ngx-spinner';
import { SidebarService } from '../../../layout/services/sidebar.service';

@Component({
  selector: 'cmdb-build-category-form',
  templateUrl: './build-category-form.component.html',
  styleUrls: ['./build-category-form.component.scss']
})
export class BuildCategoryFormComponent implements OnInit, AfterContentInit {

  @Input() categoryForm: FormGroup;
  @Input() mode: CategoryMode = CategoryMode.Create;
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
              private toast: ToastService, private modalService: NgbModal, private activateRoute: ActivatedRoute,
              private spinner: NgxSpinnerService, private sidebarService: SidebarService) {

    this.activateRoute.params.subscribe(params => {
      this.categoryID = params.publicID;
    });
  }

  ngOnInit() {
    // Create mode
    if (this.mode === CategoryMode.Create) {
      this.category = new CmdbCategory();
      this.categoryForm.get('name').setAsyncValidators(checkCategoryExistsValidator(this.categoryService));
      this.categoryForm.get('label').valueChanges.subscribe(value => {
        value = value == null ? '' : value;
        this.categoryForm.get('name').setValue(value.replace(/ /g, '-').toLowerCase());
        const newValue = this.categoryForm.get('name').value;
        this.categoryForm.get('name').setValue(newValue.replace(/[^a-z0-9 \-]/gi, '').toLowerCase());
        this.categoryForm.get('name').markAsDirty({onlySelf: true});
        this.categoryForm.get('name').markAsTouched({onlySelf: true});
      });

      this.categoryService.getCategoryList().subscribe((list: CmdbCategory[]) => {
        this.spinner.show();
        this.categoryList = list;
      }, error => {},
        () => this.spinner.hide());
    }
    // Edit mode
    if (this.mode === CategoryMode.Edit) {
      this.categoryService.getCategory(this.categoryID).subscribe(value => {
        this.category = value;
        this.spinner.show();
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
        // filter category list
        this.categoryService.getCategoryList().subscribe((list: CmdbCategory[]) => {
          this.categoryList = list;
          if (this.categoryID !== undefined && this.category !== undefined) {
            list = list.filter(item => item.public_id !== this.category.public_id);
            this.categoryList = list.filter(item => item.public_id !== this.category.parent_id);
          }
        });
        this.spinner.hide();
      });
    }
    this.typeService.getUncategorizedTypes().subscribe((typeList: CmdbType[]) => {
      this.typeList = typeList;
    });
  }

  ngAfterContentInit(): void {
    const parent: any = document.getElementsByClassName('category-form')[0];
    const first: any = document.getElementsByClassName('drag-items')[0];
    const second: any = document.getElementsByClassName('drag-items')[1];
    first.style.height = parent.offsetHeight / 1.5 + 'px';
    second.style.height = parent.offsetHeight / 1.5 + 'px';
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
    const tmpCategory: CmdbCategory = this.category;
    tmpCategory.name = this.categoryForm.get('name').value;
    tmpCategory.label = this.categoryForm.get('label').value;
    tmpCategory.parent_id = this.parentCategories.length > 0 ? this.parentCategories.pop().public_id : 0;

    if (this.mode === CategoryMode.Create) {
      this.addCategory(tmpCategory);
    } else if (this.mode === CategoryMode.Edit) {
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
        this.reloadData('Category # ' + tmpCategory.public_id + ' was created');
      });
    this.categoryForm.reset();
  }

  public editCategory(tmpCategory: CmdbCategory): void {
    this.categoryService.updateCategory(tmpCategory).subscribe((resp: number) => {
      console.log(resp);
    }, (error) => {
      console.error(error);
    }, () => {
      this.reloadData('Category # ' + tmpCategory.public_id + ' was updated');
    });
  }

  private reloadData(toastMessage: string) {
    this.categoryService.getCategoryList().subscribe((list: CmdbCategory[]) => {
      this.categoryList = list;
    }, (error) => {
      console.log(error);
    }, () => {
      this.toUpdateTypes.forEach( type => {
        type.category_id = type.category_id === undefined ? this.category.public_id : type.category_id;
        this.typeService.putType(type).subscribe((updateResp: CmdbType) => {
          console.log(updateResp.public_id);
        });
      });
      this.sidebarService.updateCategoryTree();
      this.toast.show(toastMessage);
      this.router.navigate(['/framework/category/']);
    });
  }
}
