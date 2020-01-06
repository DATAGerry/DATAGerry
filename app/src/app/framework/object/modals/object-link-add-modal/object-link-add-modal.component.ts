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

import { Component, EventEmitter, Input, OnDestroy, OnInit, Output } from '@angular/core';
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';
import { AbstractControl, FormControl, FormGroup, ValidatorFn, Validators } from '@angular/forms';
import { RenderResult } from '../../../models/cmdb-render';
import { ObjectService } from '../../../services/object.service';
import { Subscription } from 'rxjs';
import { debounceTime } from 'rxjs/operators';
import { LinkService } from '../../../services/link.service';

@Component({
  templateUrl: './object-link-add-modal.component.html',
  styleUrls: ['./object-link-add-modal.component.scss']
})
export class ObjectLinkAddModalComponent implements OnInit, OnDestroy {

  // Data
  public primaryResult: RenderResult;
  public secondaryResult: RenderResult;

  @Output() public closeEmitter: EventEmitter<string> = new EventEmitter<string>();

  @Input()
  public set primaryRenderResult(result: RenderResult) {
    this.primaryResult = result;
    this.addLinkForm.get('primary').setValue(this.primaryRenderResult.object_information.object_id);
  }

  public get primaryRenderResult(): RenderResult {
    return this.primaryResult;
  }

  // Form
  public addLinkForm: FormGroup;

  // Subscriptions
  private secondarySelectionSubscription: Subscription;
  private secondaryResultSubscription: Subscription;

  constructor(public activeModal: NgbActiveModal, private objectService: ObjectService, private linkService: LinkService) {
    this.addLinkForm = new FormGroup({
      primary: new FormControl(null, [Validators.required]),
      secondary: new FormControl('', [Validators.required, this.sameIDValidator])
    });

    this.primaryResult = undefined;
    this.secondaryResult = undefined;
  }

  public get primary() {
    return this.addLinkForm.get('primary');
  }

  public get secondary() {
    return this.addLinkForm.get('secondary');
  }

  private sameIDValidator(): ValidatorFn {
    return (control: AbstractControl): { [key: string]: any } | null => {
      const same = control.value === this.primary.value;
      return same ? { sameID: { value: control.value } } : null;
    };
  }

  public ngOnInit(): void {
    this.secondarySelectionSubscription = new Subscription();
    this.secondaryResultSubscription = new Subscription();
    this.secondarySelectionSubscription = this.addLinkForm.get('secondary').valueChanges.pipe(debounceTime(500))
      .subscribe((selectedID: number) => {
        this.addLinkForm.get('secondary').setValidators([Validators.required, this.sameIDValidator()]);
        if (selectedID !== null && this.addLinkForm.get('secondary').valid) {
          this.secondaryResultSubscription = this.objectService.getObject(selectedID).subscribe(
            (secondaryResult: RenderResult) => {
              this.secondaryResult = secondaryResult;
            },
            () => {
              this.secondaryResult = undefined;
            }
          );
        }
      });
    this.addLinkForm.get('secondary').updateValueAndValidity();
  }

  public ngOnDestroy(): void {
    this.secondarySelectionSubscription.unsubscribe();
    this.secondaryResultSubscription.unsubscribe();
  }

  public onSave() {
    const formData = this.addLinkForm.getRawValue();
    this.linkService.postLink(formData).subscribe(insertResult => {
    }).add(() => {
      this.activeModal.close();
      this.closeEmitter.emit('save');
    });
  }

}
