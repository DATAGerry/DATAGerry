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


import { Component, Input, OnInit, ViewChild} from '@angular/core';
import { CmdbType } from '../../../framework/models/cmdb-type';
import { CmdbMode } from '../../../framework/modes.enum';
import { TaskBasicStepComponent } from './task-basic-step/task-basic-step.component';
import { TaskSourcesStepComponent } from './task-sources-step/task-sources-step.component';
import { TaskDestinationsStepComponent } from './task-destinations-step/task-destinations-step.component';
import { TaskVariablesStepComponent } from './task-variables-step/task-variables-step.component';
import { TaskSchedulingStepComponent } from './task-scheduling-step/task-scheduling-step.component';
import { ExportdJob } from '../../models/exportd-job';
import { ExportdJobService } from '../../services/exportd-job.service';
import { Router } from '@angular/router';
import { ToastService } from '../../../layout/toast/toast.service';

@Component({
  selector: 'cmdb-task-settings-builder',
  templateUrl: './task-settings-builder.component.html',
  styleUrls: ['./task-settings-builder.component.scss']
})
export class TaskSettingsBuilderComponent implements OnInit {

  @Input() public mode: number = CmdbMode.Create;
  @Input() public typeInstance?: CmdbType;
  @Input() public taskInstance?: ExportdJob;

  @ViewChild(TaskBasicStepComponent, {static: true})
  public basicStep: TaskBasicStepComponent;

  @ViewChild(TaskSourcesStepComponent, {static: true})
  public sourcesStep: TaskSourcesStepComponent;

  @ViewChild(TaskDestinationsStepComponent, {static: true})
  public destinationStep: TaskDestinationsStepComponent;

  @ViewChild(TaskVariablesStepComponent, {static: true})
  public variablesStep: TaskVariablesStepComponent;

  @ViewChild(TaskSchedulingStepComponent, {static: true})
  public schedulingStep: TaskSchedulingStepComponent;

  constructor(private taskService: ExportdJobService, private router: Router, private toast: ToastService) { }

  ngOnInit() {
  }

  public saveTask() {

    if (this.mode === CmdbMode.Create) {
      this.taskInstance = new ExportdJob();
    }
    this.taskInstance.name = this.basicStep.basicForm.get('name').value;
    this.taskInstance.label = this.basicStep.basicForm.get('label').value;
    this.taskInstance.active = this.basicStep.basicForm.get('active').value;
    this.taskInstance.description = this.basicStep.basicForm.get('description').value;

    this.taskInstance.destination = this.destinationStep.destinationForm.get('destination').value;
    this.taskInstance.sources = this.sourcesStep.sourcesForm.get('sources').value;
    this.taskInstance.variables = this.variablesStep.variableForm.get('variables').value;
    this.taskInstance.scheduling = {
      event: this.schedulingStep.eventForm.value,
      cron: this.schedulingStep.cronForm.value
    };

    if (this.mode === CmdbMode.Create) {
      let newID = null;
      this.taskService.postTask(this.taskInstance).subscribe(publicIDResp => {
          newID = publicIDResp;
          this.router.navigate(['/settings/exportdjob/'], {queryParams: {typeAddSuccess: newID}});
        },
        (error) => {
          console.error(error);
        });
    } else if (this.mode === CmdbMode.Edit) {
      this.taskService.putTask(this.taskInstance).subscribe((updateResp: ExportdJob) => {
          this.toast.show(`Exportd Job was successfully edit: Exportd Job ID: ${updateResp.public_id}`);
          this.router.navigate(['/settings/exportdjob/'], {queryParams: {typeEditSuccess: updateResp.public_id}});
        },
        (error) => {
          console.log(error);
        });
    }
  }
}
