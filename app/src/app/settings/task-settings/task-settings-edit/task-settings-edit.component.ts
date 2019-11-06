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


import {Component, Input, OnInit} from '@angular/core';
import { CmdbMode } from '../../../framework/modes.enum';
import { CmdbType } from '../../../framework/models/cmdb-type';
import { TypeService } from '../../../framework/services/type.service';
import { ActivatedRoute } from '@angular/router';
import { Task } from '../../models/task';
import { TaskService } from '../../services/task.service';

@Component({
  selector: 'cmdb-task-settings-edit',
  templateUrl: './task-settings-edit.component.html',
  styleUrls: ['./task-settings-edit.component.scss']
})
export class TaskSettingsEditComponent implements OnInit {

  public taskID: number;
  public typeInstance: CmdbType;
  public taskInstance: Task;
  public mode: number = CmdbMode.Edit;

  constructor(private typeService: TypeService, private taskService: TaskService, private route: ActivatedRoute) {
    this.route.params.subscribe((id) => this.taskID = id.publicID);
  }

  public ngOnInit(): void {
    // this.typeService.getType(this.typeID).subscribe((typeInstance: CmdbType) => this.typeInstance = typeInstance);
    this.taskService.getTask(this.taskID).subscribe((taskInstance: Task) => this.taskInstance = taskInstance);
  }

}
