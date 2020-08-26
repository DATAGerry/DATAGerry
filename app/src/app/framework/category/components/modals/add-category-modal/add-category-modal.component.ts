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
* along with this program. If not, see <https://www.gnu.org/licenses/>.
*/

import { Component, Input, OnInit } from '@angular/core';
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { CmdbCategory } from '../../../../models/cmdb-category';
import { CategoryService, checkCategoryExistsValidator } from '../../../../services/category.service';
import { NgxSpinnerService } from 'ngx-spinner';

@Component({
  selector: 'cmdb-add-category-modal',
  templateUrl: './add-category-modal.component.html',
  styleUrls: ['./add-category-modal.component.scss']
})
export class AddCategoryModalComponent implements OnInit {

  public catAddForm: FormGroup;
  public categoryList: CmdbCategory[];

  constructor(public activeModal: NgbActiveModal, private spinner: NgxSpinnerService,
              private categoryService: CategoryService) {
    this.catAddForm = new FormGroup({
      name: new FormControl('', Validators.required),
      label: new FormControl('')
    });
  }

  public ngOnInit(): void {
    this.name.setAsyncValidators(checkCategoryExistsValidator(this.categoryService));
    this.categoryService.getCategoryList().subscribe((list: CmdbCategory[]) => {
        this.spinner.show();
        this.categoryList = list;
      }, error => {
      },
      () => this.spinner.hide());
  }

  public get name(): FormControl {
    return this.catAddForm.get('name') as FormControl;
  }

  public get label(): FormControl {
    return this.catAddForm.get('label') as FormControl;
  }

}
