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
import { TaskBasicStepComponent } from '../task-basic-step/task-basic-step.component';

@Component({
  selector: 'cmdb-task-complete-step',
  templateUrl: './task-complete-step.component.html',
  styleUrls: ['./task-complete-step.component.scss']
})
export class TaskCompleteStepComponent implements OnInit {

  @Input() public basicStep: TaskBasicStepComponent = null;
  constructor() { }

  ngOnInit() {
  }

}
