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

import { Component, EventEmitter, Input, OnDestroy, OnInit, Output, TemplateRef, ViewChild } from '@angular/core';
import { forkJoin, Observable, ReplaySubject } from 'rxjs';
import { NgbActiveModal, NgbModal, NgbModalRef } from '@ng-bootstrap/ng-bootstrap';
import { Column, Sort, SortDirection } from '../../../../../layout/table/table.types';
import { ExportdJobLogService } from '../../../../services/exportd-job-log.service';
import { ToastService } from '../../../../../layout/toast/toast.service';
import { CollectionParameters } from '../../../../../services/models/api-parameter';
import { ExportdLog } from '../../../../models/exportd-log';
import { ExecuteState } from '../../../../models/modes_job.enum';
import { APIGetMultiResponse } from '../../../../../services/models/api-response';
import { TableComponent } from '../../../../../layout/table/table.component';
import { RenderResult } from '../../../../../framework/models/cmdb-render';

@Component({
  selector: 'cmdb-modal-content',
  template: `
      <div class="modal-header">
          <h4 class="modal-title" id="modal-basic-title">Delete Log</h4>
          <button type="button" class="close" aria-label="Close" (click)="activeModal.dismiss('Cross click')">
              <span aria-hidden="true">&times;</span>
          </button>
      </div>
      <div class="modal-body">
          Are you sure you want to delete this log?
      </div>
      <div class="modal-footer">
          <button type="button" class="btn btn-danger" (click)="activeModal.close(this.publicID)">Delete</button>
      </div>
  `
})
export class DeleteLogJobModalComponent {

  /**
   * PublicID of the log.
   */
  @Input() public publicID: number;
  constructor(public activeModal: NgbActiveModal) {
  }
}

@Component({
  selector: 'cmdb-log-exportd-table',
  templateUrl: './log-exportd-table.component.html',
  styleUrls: ['./log-exportd-table.component.scss']
})
export class LogExportdTableComponent implements OnInit, OnDestroy {

  /**
   * Generic export parameter.
   */
  public query: Array<any>;

  @Input('query')
  public set Query(query: Array<any> | any) {
    this.query = query;
    this.loadLogsFromAPI();
  }

  /**
   * Table Template: active column.
   */
  @ViewChild('activeTemplate', { static: true }) activeTemplate: TemplateRef<any>;

  /**
   * Table Template: log date column.
   */
  @ViewChild('logDateTemplate', { static: true }) logDateTemplate: TemplateRef<any>;

  /**
   * Table Template: user column.
   */
  @ViewChild('userTemplate', { static: true }) userTemplate: TemplateRef<any>;

  /**
   * Table Template: actions column.
   */
  @ViewChild('actionsTemplate', { static: true }) actionsTemplate: TemplateRef<any>;

  /**
   * Table Template: delete column.
   */
  @ViewChild('deleteButton', { static: true }) deleteButton: TemplateRef<any>;

  /**
   * Table component.
   */
  @ViewChild(TableComponent) exportdLogsTableComponent: TableComponent<RenderResult>;

  /**
   * Component un-subscriber
   * @private
   */
  private subscriber: ReplaySubject<void> = new ReplaySubject<void>();

  /**
   * Table columns definition.
   */
  public columns: Array<Column>;

  /**
   * Delete modal ref.
   * @private
   */
  private modalRef: NgbModalRef;

  /**
   * List of displayed logs.
   */
  public logs: Array<ExportdLog> = [];

  /**
   * Total number of logs.
   */
  public totalLogs: number = 0;

  /**
   * Execution states.
   */
  public modes = ExecuteState;

  /**
   * Current selected logs.
   */
  public selectedLogs: Array<ExportdLog> = [];

  /**
   * Number of selected log ids.
   */
  public selectedLogIDs: Array<number> = [];

  /**
   * Begin with first page.
   */
  public readonly initPage: number = 1;
  public page: number = this.initPage;

  /**
   * Max number of logs per site.
   * @private
   */
  private readonly initLimit: number = 10;
  public limit: number = this.initLimit;

  /**
   * Filter query from the table search input.
   */
  public filter: string;

  /**
   * Default sort filter.
   */
  public sort: Sort = { name: 'public_id', order: SortDirection.DESCENDING } as Sort;

  /**
   * Loading indicator.
   */
  public loading: boolean = false;

  /**
   * Outputs the total number of logs.
   */
  @Output() totalLogsChange: EventEmitter<number> = new EventEmitter<number>();

  constructor(private jobLogService: ExportdJobLogService, private toast: ToastService, private modalService: NgbModal) {
  }

  public ngOnInit(): void {
    this.columns = [
      {
        display: 'Public ID',
        name: 'public_id',
        data: 'public_id',
        searchable: true,
        sortable: true
      },
      {
        display: 'Job ID',
        name: 'job_id',
        data: 'job_id',
        searchable: true,
        sortable: true
      },
      {
        display: 'Job State',
        name: 'state',
        data: 'state',
        searchable: false,
        sortable: true,
        template: this.activeTemplate,
        cssClasses: ['text-center'],
        style: { width: '6rem' }
      },
      {
        display: 'Event',
        name: 'event',
        data: 'event',
        searchable: true,
        sortable: true
      },
      {
        display: 'Action',
        name: 'action_name',
        data: 'action_name',
        searchable: true,
        sortable: true
      },
      {
        display: 'User',
        name: 'user_id',
        data: 'user_id',
        searchable: true,
        sortable: true,
        template: this.userTemplate
      },
      {
        display: 'Date',
        name: 'log_time',
        data: 'log_time',
        searchable: true,
        sortable: true,
        template: this.logDateTemplate
      },
      {
        display: 'Message',
        name: 'message',
        data: 'message',
        searchable: true,
        sortable: true
      },
      {
        display: 'Actions',
        name: 'actions',
        searchable: false,
        sortable: false,
        fixed: true,
        template: this.actionsTemplate,
        cssClasses: ['text-center'],
        cellClasses: ['actions-buttons']
      }
    ] as Array<Column>;
    this.loadLogsFromAPI();
  }

  /**
   * Load the logs from the api.
   */
  public loadLogsFromAPI() {
    this.loading = true;
    let query = [];
    query.push({
      $match: {
        log_type: 'ExportdJobLog'
      }
    });
    if (this.query) {
      query = query.concat(this.query);
    }
    if (this.filter) {
      const or = [];
      const searchableColumns = this.columns.filter(c => c.searchable);
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
          public_id: { $toString: '$public_id' },
          job_id: { $toString: '$job_id' }
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
        },
      });
      or.push({
        job_id: {
          $elemMatch: {
            value: {
              $regex: String(this.filter),
              $options: 'ismx'
            }
          }
        },
      });
      query.push({ $match: { $or: or } });
    }

    const params: CollectionParameters = {
      filter: query, limit: this.limit,
      sort: this.sort.name, order: this.sort.order, page: this.page
    };
    this.jobLogService.getLogs(params).subscribe((apiResponse: APIGetMultiResponse<ExportdLog>) => {
      this.logs = apiResponse.results as Array<ExportdLog>;
      this.totalLogs = apiResponse.total;
      this.totalLogsChange.emit(this.totalLogs);
      this.loading = false;
    });
  }

  /**
   * On table sort change.
   * Reload all logs.
   *
   * @param sort
   */
  public onSortChange(sort: Sort): void {
    this.sort = sort;
    this.loadLogsFromAPI();
  }

  /**
   * On table page change.
   * Reload all logs.
   *
   * @param page
   */
  public onPageChange(page: number) {
    this.page = page;
    this.loadLogsFromAPI();
  }

  /**
   * On table page size change.
   * Reload all logs.
   *
   * @param limit
   */
  public onPageSizeChange(limit: number): void {
    this.limit = limit;
    this.page = this.initPage;
    this.loadLogsFromAPI();
  }

  /**
   * On table search change.
   * Reload all logs.
   *
   * @param search
   */
  public onSearchChange(search: any): void {
    if (search) {
      this.filter = search;
    } else {
      this.filter = undefined;
    }
    this.page = this.initPage;
    this.loadLogsFromAPI();
  }

  /**
   * On table selection change.
   * Map selected items by the log id
   *
   * @param selectedItems
   */
  public onSelectedChange(selectedItems: Array<ExportdLog>): void {
    this.selectedLogs = selectedItems;
    this.selectedLogIDs = selectedItems.map(t => t.public_id);
  }

  /**
   * Component destroyer.
   */
  public ngOnDestroy(): void {
    this.subscriber.next();
    this.subscriber.complete();
    if (this.modalRef) {
      this.modalRef.close();
    }
  }

  /**
   * Delete a selected log
   * @param publicID
   */
  public deleteLog(publicID: number): void {
    this.modalRef = this.modalService.open(DeleteLogJobModalComponent);
    this.modalRef.componentInstance.publicID = publicID;
    this.modalRef.result.then(result => {
        this.jobLogService.deleteLog(publicID).subscribe(ack => {
            this.toast.success('Log was deleted!');
          }, (error) => {
            this.toast.error(error);
          },
          () => {
            this.loadLogsFromAPI();
          }
        );
      },
      (error) => {
        this.toast.error(error);
      });
  }

  /**
   * Delete the selected logs.
   */
  public deleteSelectedLogs(): void {
    if (this.selectedLogs.length > 0) {
      const deleteObserves: Observable<any>[] = [];
      for (const logID of this.selectedLogIDs) {
        deleteObserves.push(this.jobLogService.deleteLog(logID));
      }
      forkJoin(deleteObserves)
        .subscribe(dataArray => {
          this.toast.success('Logs deleted!');
          this.exportdLogsTableComponent.selectedItems = [];
          this.selectedLogs = [];
        }, error => this.toast.error(error), () => {
          this.loadLogsFromAPI();
        });
    }
  }

}
