/*
* DATAGERRY - OpenSource Enterprise CMDB
* Copyright (C) 2019 - 2021 NETHINKS GmbH
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

import { Component, Input, OnDestroy, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { checkTypeExistsValidator, TypeService } from '../../../services/type.service';
import { CmdbMode } from '../../../modes.enum';
import { CategoryService } from '../../../services/category.service';
import { CmdbCategory } from '../../../models/cmdb-category';
import { ReplaySubject, Subscription } from 'rxjs';
import { AddCategoryModalComponent } from '../../../category/components/modals/add-category-modal/add-category-modal.component';
import { NgbModal, NgbModalRef } from '@ng-bootstrap/ng-bootstrap';
import { SidebarService } from '../../../../layout/services/sidebar.service';
import { ToastService } from '../../../../layout/toast/toast.service';
import { CollectionParameters } from '../../../../services/models/api-parameter';
import { takeUntil } from 'rxjs/operators';
import { APIGetMultiResponse } from '../../../../services/models/api-response';


@Component({
  selector: 'cmdb-type-basic-step',
  templateUrl: './type-basic-step.component.html',
  styleUrls: ['./type-basic-step.component.scss'],
})
export class TypeBasicStepComponent implements OnInit, OnDestroy {

  private subscriber: ReplaySubject<void> = new ReplaySubject<void>();

  @Input()
  set preData(data: any) {
    if (data !== undefined) {
      this.basicForm.patchValue(data);
      this.basicMetaIconForm.patchValue(data.render_meta === undefined ? '' : data.render_meta);

      const categoryQuery: CollectionParameters = {
        filter: [{ $match: { types: { $in: [+data.public_id] } } }],
        limit: 1, sort: 'public_id', order: -1, page: 1
      };
      this.categoryService.getCategories(categoryQuery).pipe(takeUntil(this.subscriber)).subscribe((
        apiResponse: APIGetMultiResponse<CmdbCategory>) => {
          console.log(apiResponse);
          if (+apiResponse.total > 0) {
            this.originalCategoryID = apiResponse.results[0].public_id;
          } else {
            this.originalCategoryID = null;
          }
        },
        (err) => {
          this.originalCategoryID = null;
        },
        () => {
          console.log(this.originalCategoryID);
          this.basicCategoryForm.patchValue({ category_id: this.originalCategoryID });
        });
    }
  }

  @Input() public mode: CmdbMode;
  public modes = CmdbMode;

  public basicForm: FormGroup;
  public basicMetaIconForm: FormGroup;

  public basicCategoryForm: FormGroup;
  private categoriesSubscription: Subscription;
  public originalCategoryID: number = undefined;
  public categories: CmdbCategory[];
  private modalRef: NgbModalRef;

  public categoryQuery: CollectionParameters = {
    filter: undefined, limit: 0, sort: 'public_id', order: -1, page: 1
  };

  constructor(private typeService: TypeService, private categoryService: CategoryService, private modalService: NgbModal,
              private sidebarService: SidebarService, private toast: ToastService) {
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
    this.categoryService.getCategories(this.categoryQuery).pipe(takeUntil(this.subscriber)).subscribe((apiResponse: APIGetMultiResponse<CmdbCategory>) => {
      this.categories = apiResponse.results as Array<CmdbCategory>;
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
    this.subscriber.next();
    this.subscriber.complete();
    if (this.modalRef) {
      this.modalRef.close();
    }
  }

  public addCategoryModal() {
    const newCategory = new CmdbCategory();
    this.modalRef = this.modalService.open(AddCategoryModalComponent, { scrollable: true });
    this.modalRef.result.then((result: FormGroup) => {
      if (result) {
        let categoryID = null;
        newCategory.name = result.get('name').value;
        newCategory.label = result.get('label').value;
        this.categoryService.postCategory(newCategory).pipe(takeUntil(this.subscriber)).subscribe((raw: CmdbCategory) => {
            this.basicCategoryForm.get('category_id').setValue(raw.public_id);
            categoryID = raw.public_id;
          }, () => {
          },
          () => {
            this.categoryService.getCategories(this.categoryQuery).pipe(takeUntil(this.subscriber)).subscribe((apiResponse: APIGetMultiResponse<CmdbCategory>) => {
              this.categories = apiResponse.results as Array<CmdbCategory>;
            });
            this.sidebarService.loadCategoryTree();
            this.toast.success('Category # ' + categoryID + ' was created');
          });
      }
    }, (reason) => {
      console.log(reason);
    });
  }

}
