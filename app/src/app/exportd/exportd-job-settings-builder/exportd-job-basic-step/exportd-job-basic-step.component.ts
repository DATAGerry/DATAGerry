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


import { Component, Injectable, Input, OnDestroy, OnInit } from '@angular/core';
import { CmdbMode } from '../../../framework/modes.enum';
import { AbstractControl, UntypedFormControl, UntypedFormGroup, Validators } from '@angular/forms';
import { checkJobExistsValidator, ExportdJobService } from '../../exportd-job.service';
import { ExportdType } from '../../../settings/models/modes_job.enum';
import { ExportdJobBaseStepComponent } from '../exportd-job-base-step.component';
import { ReplaySubject } from 'rxjs';
import { takeUntil } from 'rxjs/operators';

@Component({
  selector: 'cmdb-task-basic-step',
  templateUrl: './exportd-job-basic-step.component.html',
  styleUrls: ['./exportd-job-basic-step.component.scss']
})
export class ExportdJobBasicStepComponent extends ExportdJobBaseStepComponent implements OnInit, OnDestroy {

  private subscriber: ReplaySubject<void> = new ReplaySubject<void>();

  @Input()
  set preData(data: any) {
    if (data !== undefined) {
      this.basicForm.patchValue(data);
    }
  }

  public basicForm: UntypedFormGroup;
  public readonly typeSelect: Array<any> = [
    { label: 'PUSH', content: ExportdType.PUSH, description: 'Run job directly.' },
    { label: 'PULL', content: ExportdType.PULL, description: 'Get the output of a job directly via REST.' }
  ];

  constructor(private exportdService: ExportdJobService) {
    super();
    this.basicForm = new UntypedFormGroup({
      name: new UntypedFormControl('', Validators.required),
      label: new UntypedFormControl('', Validators.required),
      description: new UntypedFormControl(''),
      active: new UntypedFormControl(true),
      exportd_type: new UntypedFormControl(ExportdType.PUSH)
    });
  }

  public get name() {
    return this.basicForm.get('name');
  }

  public get label() {
    return this.basicForm.get('label');
  }

  public ngOnInit(): void {
    if (this.mode === CmdbMode.Create) {
      this.basicForm.get('name').setAsyncValidators(checkJobExistsValidator(this.exportdService));
      this.basicForm.get('label').valueChanges.pipe(takeUntil(this.subscriber)).subscribe(value => {
        this.basicForm.get('name').setValue(value.replace(/ /g, '-').toLowerCase());
        this.basicForm.get('name').setValue(this.basicForm.get('name').value.replace(/[^a-z0-9 \-]/gi, '').toLowerCase());
        this.basicForm.get('name').markAsDirty({ onlySelf: true });
        this.basicForm.get('name').markAsTouched({ onlySelf: true });
      });
    } else if (CmdbMode.Edit) {
      // this.basicForm.get('name').disable();
      this.basicForm.markAllAsTouched();
    }
  }

  public ngOnDestroy(): void {
    this.subscriber.next();
    this.subscriber.complete();
  }
}
