/*
* DATAGERRY - OpenSource Enterprise CMDB
* Copyright (C) 2023 becon GmbH
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
import { CmdbType } from '../../models/cmdb-type';
import { TypeService } from '../../services/type.service';
import { ActivatedRoute, Router } from '@angular/router';
import { NgbActiveModal, NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { PreviousRouteService } from '../../../services/previous-route.service';
import { AbstractControl, UntypedFormControl, UntypedFormGroup, ValidatorFn, Validators } from '@angular/forms';
import { ToastService } from '../../../layout/toast/toast.service';


@Component({
  selector: 'cmdb-type-delete-confirm-modal',
  styleUrls: ['./type-delete.component.scss'],
  template: `
    <div class="modal-header">
      <h4 class="modal-title" id="modal-title">Type deletion</h4>
      <button type="button" class="close" aria-describedby="modal-title" (click)="modal.dismiss('Cross click')">
        <span aria-hidden="true">&times;</span>
      </button>
    </div>
    <div class="modal-body">
      <strong>Are you sure you want to delete <span class="text-primary">{{typeLabel}}</span> type?</strong>
      <!-- <p>
        All objects associated to this type will permanently deleted. <span class="text-danger">This operation can not be undone!</span>
      </p> -->
      <form id="deleteTypeModalForm" [formGroup]="deleteTypeModalForm" class="needs-validation" novalidate autocomplete="off">
        <div class="form-group">
          <label for="typeNameInput">Type the name: {{typeName}} <span class="required">*</span></label>
          <input type="text" formControlName="name" class="form-control"
                 [ngClass]="{ 'is-valid': name.valid && (name.dirty || name.touched),
                 'is-invalid': name.invalid && (name.dirty || name.touched)}"
                 id="typeNameInput" required>
          <small id="typeNameInputHelp" class="form-text text-muted">Type in the name of the type to confirm the deletion.</small>
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
      <button type="button" class="btn btn-danger" [disabled]="deleteTypeModalForm.invalid" (click)="modal.close('delete')">Delete</button>
    </div>
  `
})
export class TypeDeleteConfirmModalComponent {
  @Input() typeID: number = 0;
  @Input() typeName: string = '';
  @Input() typeLabel: string = '';

  public deleteTypeModalForm: UntypedFormGroup;

  constructor(public modal: NgbActiveModal) {

    this.deleteTypeModalForm = new UntypedFormGroup({
      name: new UntypedFormControl('', [Validators.required, this.equalName()]),
    });
  }


  public equalName(): ValidatorFn {
    return (control: AbstractControl): { [key: string]: boolean } | null => {
      if (control.value !== this.typeName) {
        return {notequal: true};
      } else {
        return null;
      }
    };
  }

  public get name() {
    return this.deleteTypeModalForm.get('name');
  }
}


@Component({
  selector: 'cmdb-type-delete',
  templateUrl: './type-delete.component.html',
  styleUrls: ['./type-delete.component.scss']
})
export class TypeDeleteComponent implements OnInit {

  public typeID: number;
  public typeInstance: CmdbType;
  public numberOfObjects: number;

  constructor(private typeService: TypeService, private router: Router, private route: ActivatedRoute,
                      public prevRoute: PreviousRouteService, private modalService: NgbModal, private toast: ToastService) {
    this.route.params.subscribe((id) => {
      this.typeID = id.publicID;
    });
  }

  public open(): void {
    const deleteModal = this.modalService.open(TypeDeleteConfirmModalComponent);
    deleteModal.componentInstance.typeID = this.typeID;
    deleteModal.componentInstance.typeName = this.typeInstance.name;
    deleteModal.componentInstance.typeLabel = this.typeInstance.label;
    deleteModal.result.then((result) => {
      if (result === 'delete') {
        this.typeService.deleteType(this.typeID).subscribe((deletedType) => {
          this.router.navigate(['/framework/type/']);
          this.toast.success(`Type was successfully Deleted: TypeID: ${ this.typeID }`);
        });
      }
    }, (reason) => {
      console.log(reason);
    });
  }


  public ngOnInit(): void {
    this.typeService.getType(this.typeID).subscribe((typeInstanceResp: CmdbType) => {
      this.typeInstance = typeInstanceResp;
    });
     this.typeService.countTypeObjects(this.typeID).subscribe((count: number) => {
      this.numberOfObjects = count;
    });
  }
}
