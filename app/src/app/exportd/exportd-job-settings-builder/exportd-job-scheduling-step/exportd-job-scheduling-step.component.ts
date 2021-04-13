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

import { Component, Input, OnInit } from '@angular/core';
import { CmdbMode } from '../../../framework/modes.enum';
import { FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { ExportdJob } from '../../../settings/models/exportd-job';

@Component({
  selector: 'cmdb-task-scheduling-step',
  templateUrl: './exportd-job-scheduling-step.component.html',
  styleUrls: ['./exportd-job-scheduling-step.component.scss']
})
export class ExportdJobSchedulingStepComponent implements OnInit {

  @Input()
  set preData(data: ExportdJob) {
    if (data !== undefined && data.scheduling !== undefined ) {
      this.eventForm.patchValue(data.scheduling.event);
      this.taskType = data.exportd_type;
    }
  }

  @Input() public mode: CmdbMode;
  public eventForm: FormGroup;
  public taskType: any;

  constructor(private formBuilder: FormBuilder) {
    this.eventForm = this.formBuilder.group({
      active: new FormControl(false, Validators.required),
    });
  }

  ngOnInit() {
    if (this.mode === CmdbMode.Edit) {
      this.eventForm.markAllAsTouched();
    }
  }
}
