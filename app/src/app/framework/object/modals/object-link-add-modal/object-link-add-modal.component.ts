/*
* DATAGERRY - OpenSource Enterprise CMDB
* Copyright (C) 2019 - 2020 NETHINKS GmbH
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

import { Component, EventEmitter, Input, OnDestroy, OnInit, Output } from '@angular/core';
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';
import { AbstractControl, FormControl, FormGroup, ValidatorFn, Validators } from '@angular/forms';
import { RenderResult } from '../../../models/cmdb-render';
import { checkObjectExistsValidator, ObjectService } from '../../../services/object.service';
import { ReplaySubject } from 'rxjs';
import { takeUntil } from 'rxjs/operators';
import { LinkService } from '../../../services/link.service';
import { ToastService } from '../../../../layout/toast/toast.service';

@Component({
  templateUrl: './object-link-add-modal.component.html',
  styleUrls: ['./object-link-add-modal.component.scss']
})
export class ObjectLinkAddModalComponent implements OnInit, OnDestroy {

  private subscriber: ReplaySubject<void> = new ReplaySubject<void>();

  public primaryResult: RenderResult;

  @Output() public closeEmitter: EventEmitter<string> = new EventEmitter<string>();

  @Input('primaryResult')
  public set primaryRenderResult(result: RenderResult) {
    this.primaryResult = result;
    this.form.get('primary').setValue(this.primaryResult.object_information.object_id);
  }

  public form: FormGroup;

  private sameIDValidator(): ValidatorFn {
    return (control: AbstractControl): { [key: string]: any } | null => {
      const same = control.value === this.primary.value;
      return same ? { sameID: { value: control.value } } : null;
    };
  }

  constructor(public activeModal: NgbActiveModal, private objectService: ObjectService, private linkService: LinkService,
              private toast: ToastService) {
    this.form = new FormGroup({
      primary: new FormControl(null, [Validators.required]),
      secondary: new FormControl('', [Validators.required, this.sameIDValidator],
        [checkObjectExistsValidator(objectService)])
    });
  }

  public get primary(): FormControl {
    return this.form.get('primary') as FormControl;
  }

  public get secondary(): FormControl {
    return this.form.get('secondary') as FormControl;
  }

  public ngOnInit(): void {
    this.form.get('secondary').updateValueAndValidity();
  }

  public onSave(): void {
    const formData = this.form.getRawValue();
    if (this.form.valid) {
      this.linkService.postLink(formData).pipe(takeUntil(this.subscriber)).subscribe(() => {
        this.toast.success(`Object #${ formData.primary } linked with #${ formData.secondary }.`);
        this.closeEmitter.emit('save');
      });
      this.activeModal.close();
    }
  }

  public ngOnDestroy(): void {
    this.subscriber.next();
    this.subscriber.complete();
  }

}
