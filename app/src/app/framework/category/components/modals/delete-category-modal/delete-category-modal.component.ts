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

import {Component, Input, OnDestroy} from '@angular/core';
import {NgbActiveModal, NgbModalRef} from '@ng-bootstrap/ng-bootstrap';
import { CmdbCategory } from '../../../../models/cmdb-category';
import { AbstractControl, FormControl, FormGroup, ValidatorFn, Validators } from '@angular/forms';

@Component({
  selector: 'cmdb-category-delete',
  template: `
    <div class="modal-header">
      <h4 class="modal-title" id="modal-title">Category deletion</h4>
      <button type="button" class="close" (click)="modal.dismiss('')">
        <span aria-hidden="true">&times;</span>
      </button>
    </div>
    <div class="modal-body">
      <strong>Are you sure you want to delete <span class="text-primary">{{category.name}}</span> category?</strong>
      <p>
        All types inside this category will be un assigned <span
        class="text-danger">This operation can not be undone!</span>
      </p>
      <form id="deleteCategoryModalForm" [formGroup]="deleteCategoryModalForm" class="needs-validation" novalidate
            autocomplete="off">
        <div class="form-group">
          <label for="categoryNameInput">Type in the name: {{category.name}} <span class="required">*</span></label>
          <input type="text" formControlName="name" class="form-control"
                 [ngClass]="{ 'is-valid': name.valid && (name.dirty || name.touched),
                 'is-invalid': name.invalid && (name.dirty || name.touched)}"
                 id="categoryNameInput" required>
          <small id="categoryNameInputHelp" class="form-text text-muted">Type in the name of the category to confirm the
            deletion.</small>
          <div *ngIf="name.invalid && (name.dirty || name.touched)"
               class="invalid-feedback">
            <div class="float-right" *ngIf="name.errors.required">
              Name is required
            </div>
            <div class="float-right" *ngIf="name.errors.notequal">
              Your answer is not equal!
            </div>
          </div>
          <div class="clearfix"></div>
        </div>
      </form>
    </div>
    <div class="modal-footer">
      <button type="button" class="btn btn-outline-secondary" (click)="modal.dismiss('cancel')">Cancel</button>
      <button type="button" class="btn btn-danger" [disabled]="deleteCategoryModalForm.invalid"
              (click)="modal.close('delete')">Delete
      </button>
    </div>
  `
})
export class DeleteCategoryModalComponent implements OnDestroy {

  constructor(public modal: NgbActiveModal) {
    this.deleteCategoryModalForm = new FormGroup({
      name: new FormControl('', [Validators.required, this.equalName()]),
    });
  }

  public get name(): FormControl {
    return this.deleteCategoryModalForm.get('name') as FormControl;
  }

  @Input() public category: CmdbCategory;
  public deleteCategoryModalForm: FormGroup;
  private modalRef: NgbModalRef;

  public ngOnDestroy(): void {
    if (this.modalRef) {
      this.modalRef.close();
    }
  }

  public equalName(): ValidatorFn {
    return (control: AbstractControl): { [key: string]: boolean } | null => {
      if (this.category) {
        if (control.value !== this.category.name) {
          return { notequal: true };
        } else {
          return null;
        }
      }

    };
  }

}
