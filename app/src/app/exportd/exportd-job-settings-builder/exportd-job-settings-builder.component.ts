/*
* DATAGERRY - OpenSource Enterprise CMDB
* Copyright (C) 2019 - 2021 NETHINKS GmbH
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


import { Component, Input, OnDestroy, OnInit, ViewChild } from '@angular/core';
import { CmdbType } from '../../framework/models/cmdb-type';
import { CmdbMode } from '../../framework/modes.enum';
import { ExportdJobBasicStepComponent } from './exportd-job-basic-step/exportd-job-basic-step.component';
import { ExportdJobSourcesStepComponent } from './exportd-job-sources-step/exportd-job-sources-step.component';
import { ExportdJobDestinationsStepComponent } from './exportd-job-destinations-step/exportd-job-destinations-step.component';
import { ExportdJobVariablesStepComponent } from './exportd-job-variables-step/exportd-job-variables-step.component';
import { ExportdJobSchedulingStepComponent } from './exportd-job-scheduling-step/exportd-job-scheduling-step.component';
import { ExportdJob } from '../../settings/models/exportd-job';
import { ExportdJobService } from '../exportd-job.service';
import { Router } from '@angular/router';
import { ToastService } from '../../layout/toast/toast.service';
import { TypeService } from '../../framework/services/type.service';
import { ReplaySubject } from 'rxjs';
import { takeUntil } from 'rxjs/operators';
import { APIGetMultiResponse } from '../../services/models/api-response';
import { CollectionParameters } from '../../services/models/api-parameter';

@Component({
  selector: 'cmdb-task-settings-builder',
  templateUrl: './exportd-job-settings-builder.component.html',
  styleUrls: ['./exportd-job-settings-builder.component.scss']
})
export class ExportdJobSettingsBuilderComponent implements OnInit, OnDestroy {

  private subscriber: ReplaySubject<void> = new ReplaySubject<void>();

  public types: Array<CmdbType> = [];
  public typeParams: CollectionParameters = { filter: undefined, limit: 10, sort: 'public_id', order: 1, page: 1 };
  public apiTypeResponse: APIGetMultiResponse<CmdbType>;
  public totalTypes: number = 0;
  private currentPage: number;

  @Input() public mode: number = CmdbMode.Create;
  @Input() public task?: ExportdJob;

  @ViewChild(ExportdJobBasicStepComponent, { static: true })
  public basicStep: ExportdJobBasicStepComponent;

  @ViewChild(ExportdJobSourcesStepComponent, { static: true })
  public sourcesStep: ExportdJobSourcesStepComponent;

  @ViewChild(ExportdJobDestinationsStepComponent, { static: true })
  public destinationStep: ExportdJobDestinationsStepComponent;

  @ViewChild(ExportdJobVariablesStepComponent, { static: true })
  public variablesStep: ExportdJobVariablesStepComponent;

  @ViewChild(ExportdJobSchedulingStepComponent, { static: true })
  public schedulingStep: ExportdJobSchedulingStepComponent;

  constructor(private taskService: ExportdJobService, private router: Router,
              private typeService: TypeService, private toast: ToastService) {
  }

  public ngOnInit(): void {
    const typesCallParameters: CollectionParameters = {
      filter: undefined,
      limit: 0,
      sort: 'public_id',
      order: 1,
      page: 1
    };
    this.typeService.getTypes(typesCallParameters).pipe(takeUntil(this.subscriber))
      .subscribe((response: APIGetMultiResponse) => {
        this.types = response.results as Array<CmdbType>;
      });
    // this.onLoadTypes();
  }

  public onLoadTypes(): void {
    if (!this.currentPage) {
      this.typeService.getTypes(this.typeParams).pipe(takeUntil(this.subscriber)).subscribe(
        (apiResponse: APIGetMultiResponse<CmdbType>) => {
          this.apiTypeResponse = apiResponse;
          this.currentPage = 1;
          this.totalTypes = this.apiTypeResponse.total;
          this.types = [...this.types, ...apiResponse.results as Array<CmdbType>];
        });
    } else if (this.currentPage <= this.apiTypeResponse.pager.total_pages) {
      this.currentPage += 1;
      this.typeParams.page = this.currentPage;
      this.typeService.getTypes(this.typeParams).pipe(takeUntil(this.subscriber)).subscribe(
        (apiResponse: APIGetMultiResponse<CmdbType>) => {
          this.types = [...this.types, ...apiResponse.results as Array<CmdbType>];
        });
    }
  }

  public saveTask(): void {
    if (this.mode === CmdbMode.Create) {
      this.task = new ExportdJob();
    }
    this.task.name = this.basicStep.basicForm.get('name').value;
    this.task.label = this.basicStep.basicForm.get('label').value;
    this.task.active = this.basicStep.basicForm.get('active').value;
    this.task.exportd_type = this.basicStep.basicForm.get('exportd_type').value;
    this.task.description = this.basicStep.basicForm.get('description').value;

    this.task.destination = this.destinationStep.destinationForm.get('destination').value;
    this.task.sources = this.sourcesStep.sourcesForm.get('sources').value;
    this.task.variables = this.variablesStep.variableForm.get('variables').value;
    this.task.scheduling = { event: this.schedulingStep.eventForm.value };

    if (this.mode === CmdbMode.Create) {
      this.taskService.postTask(this.task).pipe(takeUntil(this.subscriber)).subscribe((job: ExportdJob) => {
          this.router.navigate(['/exportd/'], { queryParams: { typeAddSuccess: job.public_id } });
        },
        (error) => {
          this.toast.error(error.message);
        });
    } else if (this.mode === CmdbMode.Edit) {
      this.taskService.putTask(this.task).pipe(takeUntil(this.subscriber)).subscribe((job: ExportdJob) => {
          this.toast.success(`Exportd Job was successfully edited: Exportd Job ID: ${ job.public_id }`);
          this.router.navigate(['/exportd/'], { queryParams: { typeEditSuccess: job.public_id } });
        },
        (error) => {
          this.toast.error(error.message);
        });
    }
  }

  public ngOnDestroy(): void {
    this.subscriber.next();
    this.subscriber.complete();
  }
}
