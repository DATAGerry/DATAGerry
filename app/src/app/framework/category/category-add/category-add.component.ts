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
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { CategoryMode } from '../../modes.enum';
import { CategoryService } from '../../services/category.service';
import { CmdbCategory } from '../../models/cmdb-category';

@Component({
  selector: 'cmdb-category-add',
  templateUrl: './category-add.component.html',
  styleUrls: ['./category-add.component.scss']
})
export class CategoryAddComponent implements OnInit {

  public categoryAddForm: FormGroup;
  public mode = CategoryMode.Create;

  constructor(private categoryService: CategoryService) {}

  ngOnInit() {
    this.categoryAddForm = new FormGroup({
      name: new FormControl('', Validators.required),
      label: new FormControl('', Validators.required),
      root: new FormControl({value: false, disabled: true}, Validators.required)
    });

    this.categoryService.getRootCategory().subscribe((category: CmdbCategory[]) => {
      this.categoryAddForm.get('root').setValue(!category.length);
    });
  }

}
