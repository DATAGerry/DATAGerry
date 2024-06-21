/*
* DATAGERRY - OpenSource Enterprise CMDB
* Copyright (C) 2024 becon GmbH
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
*
* You should have received a copy of the GNU Affero General Public License
* along with this program. If not, see <https://www.gnu.org/licenses/>.
*/
import { Component, OnDestroy, OnInit, TemplateRef, ViewChild } from '@angular/core';
import { ActivatedRoute, Data, Router } from '@angular/router';

import { BehaviorSubject, ReplaySubject, takeUntil } from 'rxjs';

import { NgbModal, NgbModalRef } from '@ng-bootstrap/ng-bootstrap';

import { ExportdJobService } from '../exportd-job.service';
import { ToastService } from '../../layout/toast/toast.service';
import { PermissionService } from '../../modules/auth/services/permission.service';
import { UserSettingsDBService } from '../../management/user-settings/services/user-settings-db.service';
import {
  convertResourceURL,
  UserSettingsService
} from '../../management/user-settings/services/user-settings.service';

import { ExportdJob } from '../../settings/models/exportd-job';
import { ExecuteState, ExportdType } from '../../settings/models/modes_job.enum';
import { GeneralModalComponent } from '../../layout/helpers/modals/general-modal/general-modal.component';
import { APIGetMultiResponse } from '../../services/models/api-response';
import { CollectionParameters } from '../../services/models/api-parameter';
import { Column, Sort, SortDirection, TableState, TableStatePayload } from '../../layout/table/table.types';

import { UserSetting } from '../../management/user-settings/models/user-setting';
/* ------------------------------------------------------------------------------------------------------------------ */

@Component({
    selector: 'cmdb-task-settings-list',
    templateUrl: './exportd-job-settings-list.component.html',
    styleUrls: ['./exportd-job-settings-list.component.scss']
})
export class ExportdJobSettingsListComponent implements OnInit, OnDestroy {

    // HTML ID of the table. Used for user settings and table-states
    public readonly id: string = 'exportd-jobs-table';

    private subscriber: ReplaySubject<void> = new ReplaySubject<void>();

    // Table Template: active column
    @ViewChild('activeTemplate', { static: true }) activeTemplate: TemplateRef<any>;

    // Table Template: type column
    @ViewChild('typeTemplate', { static: true }) typeTemplate: TemplateRef<any>;

    // Table Template: destination column
    @ViewChild('destinationTemplate', { static: true }) destinationTemplate: TemplateRef<any>;

    // Table Template: running column
    @ViewChild('runningTemplate', { static: true }) runningTemplate: TemplateRef<any>;

    // Table Template: execution column
    @ViewChild('executionDateTemplate', { static: true }) executionDateTemplate: TemplateRef<any>;

    // Table Template: user column
    @ViewChild('userTemplate', { static: true }) userTemplate: TemplateRef<any>;

    // Table Template: job run column
    @ViewChild('jobRunTemplate', { static: true }) jobRunTemplate: TemplateRef<any>;

    // Table Template: job run state column
    @ViewChild('jobRunStateTemplate', { static: true }) jobRunStateTemplate: TemplateRef<any>;

    // Table Template: log state column
    @ViewChild('logTemplate', { static: true }) logTemplate: TemplateRef<any>;

    // Table Template: action column
    @ViewChild('actionTemplate', { static: true }) actionTemplate: TemplateRef<any>;

    // Table Buttons: add button
    @ViewChild('addButton', { static: true }) addButton: TemplateRef<any>;


    public columns: Array<Column> = [];

    public tasks: Array<ExportdJob> = [];
    public tasksAPIResponse: APIGetMultiResponse<ExportdJob>;
    public totalTasks: number = 0;

    // Begin with first page
    public readonly initPage: number = 1;
    public page: number = this.initPage;

    // Max number of types per site
    private readonly initLimit: number = 10;
    public limit: number = this.initLimit;

    // Filter query from the table search input
    public filter: string;

    public sort: Sort = { name: 'public_id', order: SortDirection.DESCENDING } as Sort;

    // Loading indicator
    public loading: boolean = false;

    public tableStateSubject: BehaviorSubject<TableState> = new BehaviorSubject<TableState>(undefined);
    public tableStates: Array<TableState> = [];

    public initialVisibleColumns: Array<string> = [];

    public modes = ExecuteState;
    public typeMode = ExportdType;
    private modalRef: NgbModalRef;
  
    public messageBlock: string = 'Exportd is an interface for exporting objects to external systems like monitoring systems,\n' +
      'ticket systems, backup software or any kind of other system. Exports are organized in Jobs. A Job contains Sources,\n' +
      'Destinations and Variables. Export Jobs can be triggered manually (by clicking on a button in the webui) or event based,\n' +
      'if the configured sources of a job were changed (e.g. a new object was added). Export Jobs can be of type Push (default)\n' +
      ' or Pull. Push Jobs are a push to an external system, which runs in a background process, while a Pull job is triggered\n' +
      ' by an external system via REST. The client directly gets the result within that REST call.';

/* -------------------------------------------------- GETTER/SETTER ------------------------------------------------- */

    public get tableState(): TableState {
        return this.tableStateSubject.getValue() as TableState;
    }

/* ------------------------------------------------------------------------------------------------------------------ */
/*                                                     LIFE CYCLE                                                     */
/* ------------------------------------------------------------------------------------------------------------------ */

    constructor(
        private taskService: ExportdJobService,
        private router: Router,
        private route: ActivatedRoute,
        private userSettingsService: UserSettingsService<UserSetting, TableStatePayload>,
        private indexDB: UserSettingsDBService<UserSetting, TableStatePayload>,
        private toast: ToastService,
        private modalService: NgbModal,
        private permissionService: PermissionService
    ) {

        this.route.data.pipe(takeUntil(this.subscriber)).subscribe((data: Data) => {
            if (data.userSetting) {
                const userSettingPayloads = (data.userSetting as UserSetting<TableStatePayload>).payloads
                                            .find(payloads => payloads.id === this.id);
                this.tableStates = userSettingPayloads.tableStates;
                this.tableStateSubject.next(userSettingPayloads.currentState);
            } else {
                this.tableStates = [];
                this.tableStateSubject.next(undefined);

                const statePayload: TableStatePayload = new TableStatePayload(this.id, []);
                const resource: string = convertResourceURL(this.router.url.toString());
                const userSetting = this.userSettingsService.createUserSetting<TableStatePayload>(resource, [statePayload]);
                this.indexDB.addSetting(userSetting);
            }
        });
    }


    public ngOnInit(): void {
        const columns = [
            {
                display: 'Active',
                name: 'active',
                data: 'active',
                searchable: false,
                sortable: true,
                template: this.activeTemplate,
                cssClasses: ['text-center'],
                style: { width: '6rem' }
            },
            {
                display: 'Public ID',
                name: 'public_id',
                data: 'public_id',
                searchable: true,
                sortable: true
            },
            {
                display: 'Type',
                name: 'exportd_type',
                data: 'exportd_type',
                searchable: false,
                sortable: true,
                template: this.typeTemplate,
            },
            {
                display: 'Name',
                name: 'name',
                data: 'name',
                searchable: true,
                sortable: true
            },
            {
                display: 'Label',
                name: 'label',
                data: 'label',
                searchable: true,
                sortable: true
            },
            {
                display: 'External Systems',
                name: 'destination',
                data: 'destination',
                template: this.destinationTemplate,
                searchable: false,
                sortable: true
            },
            {
                display: 'Author',
                name: 'author_id',
                data: 'author_id',
                searchable: true,
                sortable: true,
                template: this.userTemplate
            },
            {
                display: 'Running',
                name: 'state',
                data: 'state',
                template: this.runningTemplate,
                searchable: false,
                sortable: false
            },
            {
                display: 'Last Execute Date',
                name: 'last_execute_date',
                data: 'last_execute_date',
                template: this.executionDateTemplate,
                searchable: false,
                sortable: true
            },
            {
                display: 'Execute State',
                name: 'state',
                data: 'state',
                template: this.jobRunStateTemplate,
                searchable: false,
                sortable: true
            }
        ] as Array<Column>;

        const jobRunRight = 'base.exportd.job.run';
        if (this.permissionService.hasRight(jobRunRight) || this.permissionService.hasExtendedRight(jobRunRight)) {
            columns.push({
                display: 'Execute Job',
                name: 'exportd_type',
                data: 'exportd_type',
                searchable: false,
                sortable: false,
                template: this.jobRunTemplate,
            } as Column);
        }

        const editRight = 'base.exportd.job.edit';
        if (this.permissionService.hasRight(editRight) || this.permissionService.hasExtendedRight(editRight)) {
            columns.push({
                display: 'Logs',
                name: 'public_id',
                data: 'public_id',
                searchable: false,
                sortable: false,
                template: this.logTemplate,
            } as Column);
        }

        const logRight = 'base.exportd.log.view';
        if (this.permissionService.hasRight(logRight) || this.permissionService.hasExtendedRight(logRight)) {
            columns.push({
                display: 'Actions',
                name: 'actions',
                data: 'public_id',
                searchable: false,
                sortable: false,
                fixed: true,
                template: this.actionTemplate,
                cssClasses: ['text-center'],
                cellClasses: ['actions-buttons']
            } as Column);
        }

        this.initialVisibleColumns = columns.filter(c => !c.hidden).map(c => c.name);
        this.columns = [...columns];
        this.initTable();
        this.loadsTasksFromAPI();
    }


    public ngOnDestroy(): void {
        this.subscriber.next();
        this.subscriber.complete();

        if (this.modalRef) {
            this.modalRef.close();
        }
    }

/* ------------------------------------------------- HELPER METHODS ------------------------------------------------- */

    private initTable() {
        if (this.tableState) {
            this.sort = this.tableState.sort;
            this.page = this.tableState.page;
            this.limit = this.tableState.pageSize;
        }
    }


    private loadsTasksFromAPI() {
        this.loading = true;
        let query;

        if (this.filter) {
            query = [];
            const or = [];
            const searchableColumns = this.columns.filter(c => c.searchable);

            // Searchable Columns
            for (const column of searchableColumns) {
                const regex: any = {};
                regex[column.name] = {
                    $regex: String(this.filter),
                    $options: 'ismx'
                };

                or.push(regex);
            }

            query.push({
                $addFields: {
                    public_id: { $toString: '$public_id' }
                }
            });

            or.push({
                public_id: {
                    $elemMatch: {
                        value: {
                            $regex: String(this.filter),
                            $options: 'ismx'
                        }
                    }
                }
            });

            query.push({ $match: { $or: or } });
        }

        const params: CollectionParameters = {
            filter: query,
            limit: this.limit,
            sort: this.sort.name,
            order: this.sort.order,
            page: this.page
        };

        this.taskService.getTasks(params).pipe(takeUntil(this.subscriber))
        .subscribe((apiResponse: APIGetMultiResponse<ExportdJob>) => {
            this.tasksAPIResponse = apiResponse;
            this.tasks = apiResponse.results as Array<ExportdJob>;
            this.totalTasks = apiResponse.total;
            this.loading = false;
        });
    }


    public run_job_manual(job: ExportdJob) {
        job.running = true;
        job.state = ExecuteState.RUNNING;
        this.taskService.run_task(job.public_id).pipe(takeUntil(this.subscriber))
        .subscribe({
            next: resp => console.log(resp),
            error:  error => this.toast.error(error.message),
            complete: () => {
                this.toast.success('Job started');
                this.loadsTasksFromAPI();
            }
        });
    }


    /**
     * On table sort change.
     * Reload all tasks.
     *
     * @param sort
     */
    public onSortChange(sort: Sort): void {
        this.sort = sort;
        this.loadsTasksFromAPI();
    }


    /**
     * On table State change.
     * Update state.
     */
    public onStateChange(state: TableState): void {
        this.tableStateSubject.next(state);
    }


    /**
     * On table state reset.
     * Reset State.
     */
    public onStateReset(): void {
        this.limit = this.initLimit;
        this.page = this.initPage;
        this.sort = { name: 'public_id', order: SortDirection.DESCENDING } as Sort;
        this.tableStateSubject.next(undefined);
        this.loadsTasksFromAPI();
    }


    /**
     * On State Select.
     * Updates table settings according to the given table state
     * @param state
     */
    public onStateSelect(state: TableState) {
        this.tableStateSubject.next(state);
        this.page = this.tableState.page;
        this.limit = this.tableState.pageSize;
        this.sort = this.tableState.sort;

        for (const col of this.columns) {
            col.hidden = !this.tableState.visibleColumns.includes(col.name);
        }

        this.tableStateSubject.next(state);
        this.loadsTasksFromAPI();
    }


    /**
     * On table page change.
     * Reload all tasks.
     *
     * @param page
     */
    public onPageChange(page: number) {
        this.page = page;
        this.loadsTasksFromAPI();
    }


    /**
     * On table page size change.
     * Reload all tasks.
     *
     * @param limit
     */
    public onPageSizeChange(limit: number): void {
        this.limit = limit;
        this.page = this.initPage;
        this.loadsTasksFromAPI();
    }


    /**
     * On table search change.
     * Reload all tasks.
     *
     * @param search
     */
    public onSearchChange(search: any): void {
        this.page = this.initPage;

        if (search) {
            this.filter = search;
        } else {
            this.filter = undefined;
        }

        this.loadsTasksFromAPI();
    }


    public delTask(itemID: number) {

        this.modalRef = this.modalService.open(GeneralModalComponent);
        this.modalRef.componentInstance.title = 'Delete Exportd Job';
        this.modalRef.componentInstance.modalMessage = 'Are you sure you want to delete this Exportd Job?';
        this.modalRef.componentInstance.buttonDeny = 'Cancel';
        this.modalRef.componentInstance.buttonAccept = 'Delete';

        this.modalRef.result.then((result) => {
            if (result) {
                this.taskService.deleteTask(itemID).pipe(takeUntil(this.subscriber))
                .subscribe({
                    next: resp => this.toast.success('Task deleted!'),
                    error: error => this.toast.error(`Error while deleting task: ${ error }`),
                    complete: () => this.loadsTasksFromAPI()
                });
            }
        });
    }


    public showAlert(): void {
        $('#infobox').show();
    }
}