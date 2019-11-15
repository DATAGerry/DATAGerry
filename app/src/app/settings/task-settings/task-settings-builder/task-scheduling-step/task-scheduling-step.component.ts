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
import { CmdbMode } from '../../../../framework/modes.enum';
import { FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'cmdb-task-scheduling-step',
  templateUrl: './task-scheduling-step.component.html',
  styleUrls: ['./task-scheduling-step.component.scss']
})
export class TaskSchedulingStepComponent implements OnInit {

  @Input()
  set preData(data: any) {
    if (data !== undefined && data.scheduling !== undefined ) {
      this.eventForm.patchValue(data.scheduling.event);
      this.cronForm.patchValue(data.scheduling.cron);
    }
  }

  @Input() public mode: CmdbMode;
  public cronForm: FormGroup;
  public eventForm: FormGroup;
  public pattern: string = '^(\\*|([0-9]|1[0-9]|2[0-9]|3[0-9]|4[0-9]|5[0-9])' +
    '|\\*\\/([0-9]|1[0-9]|2[0-9]|3[0-9]|4[0-9]|5[0-9])) (\\*|([0-9]|1[0-9]|2[0-3])|' +
    '\\*\\/([0-9]|1[0-9]|2[0-3])) (\\*|([1-9]|1[0-9]|2[0-9]|3[0-1])' +
    '|\\*\\/([1-9]|1[0-9]|2[0-9]|3[0-1])) ' +
    '(\\*|([1-9]|1[0-2])|\\*\\/([1-9]|1[0-2])) (\\*|([0-7])|\\*\\/([0-7]))$';

  public expression: any[] = [
    { label: 'At every minute. ( * * * * * )', value: '* * * * *'},
    { label: 'At 12:00 every day. (0 12 * * *)', value: '0 12 * * *'},
    { label: 'At 12:00 on day-of-month 1. (0 12 1 * *)', value: '0 12 1 * *'},
    { label: 'At 11:59 on Sunday. (59 11 * * 7)', value: '59 11 * * 7'},
  ];

  constructor(private formBuilder: FormBuilder) {
    this.eventForm = this.formBuilder.group({
      active: new FormControl(false, Validators.required),
      command: new FormControl('')
    });

    this.cronForm = this.formBuilder.group({
      active: new FormControl(false, Validators.required),
      expression: new FormControl('* * * * *')
    });
  }

  ngOnInit() {
    if (this.mode === CmdbMode.Edit) {
      this.eventForm.markAllAsTouched();
      this.cronForm.markAllAsTouched();
    }
  }
}
