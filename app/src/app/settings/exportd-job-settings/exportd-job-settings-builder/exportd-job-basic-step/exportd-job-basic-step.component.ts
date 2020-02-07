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


import { Component, Injectable, Input, OnInit} from '@angular/core';
import { CmdbMode } from '../../../../framework/modes.enum';
import { AbstractControl, FormControl, FormGroup, Validators} from '@angular/forms';
import { checkJobExistsValidator, ExportdJobService} from '../../../services/exportd-job.service';
import { ExportdType} from '../../../models/modes_job.enum';

@Component({
  selector: 'cmdb-task-basic-step',
  templateUrl: './exportd-job-basic-step.component.html',
  styleUrls: ['./exportd-job-basic-step.component.scss']
})
export class ExportdJobBasicStepComponent implements OnInit {

  @Input()
  set preData(data: any) {
    if (data !== undefined) {
      this.basicForm.patchValue(data);
    }
  }

  @Input() public mode: CmdbMode;
  public modes = CmdbMode;
  public basicForm: FormGroup;
  public readonly typeSelect: any[] = [
    {label: 'PUSH', content: ExportdType.PUSH, description: 'Run job directly.'},
    {label: 'PULL', content: ExportdType.PULL, description: 'Get the output of a job directly via REST.'}
    ];

  constructor(private exportdService: ExportdJobService) {
    this.basicForm = new FormGroup({
      name: new FormControl('', Validators.required),
      label: new FormControl('', Validators.required),
      description: new FormControl(''),
      active: new FormControl(true),
      exportd_type: new FormControl(ExportdType.PUSH)
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
      this.basicForm.get('label').valueChanges.subscribe(value => {
        this.basicForm.get('name').setValue(value.replace(/ /g, '-').toLowerCase());
        this.basicForm.get('name').markAsDirty({ onlySelf: true });
        this.basicForm.get('name').markAsTouched({ onlySelf: true });
      });
    } else if (CmdbMode.Edit) {
      this.basicForm.markAllAsTouched();
    }
  }
}
