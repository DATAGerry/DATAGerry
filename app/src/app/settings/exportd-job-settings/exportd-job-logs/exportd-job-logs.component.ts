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

import {Component, Input, OnDestroy, OnInit, ViewChild} from '@angular/core';
import { ExportdJobService } from '../../services/exportd-job.service';
import { ActivatedRoute } from '@angular/router';
import { DataTableDirective } from 'angular-datatables';
import {forkJoin, Observable, Subject} from 'rxjs';
import { ExecuteState } from '../../models/modes_job.enum';
import { NgbActiveModal, NgbModal} from '@ng-bootstrap/ng-bootstrap';
import { ToastService } from '../../../layout/toast/toast.service';
import { ExportdJobLogService } from '../../services/exportd-job-log.service';
import { ExportdLog } from '../../models/exportd-log';

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
  @Input() publicID: number;

  constructor(public activeModal: NgbActiveModal) {
  }
}

@Component({
  selector: 'cmdb-task-logs',
  templateUrl: './exportd-job-logs.component.html',
  styleUrls: ['./exportd-job-logs.component.scss']
})
export class ExportdJobLogsComponent implements OnInit, OnDestroy {

  @ViewChild(DataTableDirective)
  public dtElement: DataTableDirective;
  public dtOptions: any = {};
  public dtTrigger: Subject<any> = new Subject();

  public taskID: number;
  public jobLogs: ExportdLog[];
  public existingLength: number = 0;
  public modes = ExecuteState;
  public selectedObjects: number[] = [];

  public cleanupProgress: number = 0;
  public cleanupInProgress: boolean = false;

  constructor( private jobLogService: ExportdJobLogService, private route: ActivatedRoute,
               private modalService: NgbModal, private toastService: ToastService) {
    this.route.params.subscribe((id) => this.taskID = id.publicID);
  }

  public ngOnInit(): void {
    this.dtOptions = {
      ordering: true,
      order: [[1, 'desc']],
      columnDefs: [ {
        orderable: false,
        className: 'select-checkbox',
        targets:   0
      } ],
      rowCallback: (row: Node, data: any[]) => {
        const self = this;
        $('td:first-child', row).unbind('click');
        $('td:first-child', row).bind('click', () => {
          self.updateDisplay(data[1]);
        });
        return row;
      },
      select: {
        style:    'multi',
        selector: 'td:first-child'
      },
      dom:
        '<"row" <"col-sm-2" l> <"col-sm-3" B > <"col" f> >' +
        '<"row" <"col-sm-12"tr>>' +
        '<\"row\" <\"col-sm-12 col-md-5\"i> <\"col-sm-12 col-md-7\"p> >',
      buttons: [],
      orderFixed: [3, 'desc'],
      rowGroup: {
        enable: true,
        endRender(rows) {
          return `Number of logs in this action: ${ rows.count() }`;
        },
        dataSrc: 3
      },
      language: {
        search: '',
        searchPlaceholder: 'Filter...'
      }
    };
    this.jobLogService.getJobLogs(this.taskID).subscribe((logs: ExportdLog[]) => {
      console.log('RESULT');
      console.log(logs);
      this.jobLogs = logs;
      this.existingLength = this.jobLogs.length;
      this.dtTrigger.next();
    });
  }

  public delLog(publicID: number) {
    const deleteModalRef = this.modalService.open(DeleteLogJobModalComponent);
    deleteModalRef.componentInstance.publicID = publicID;
    deleteModalRef.result.then(result => {
        this.jobLogService.deleteLog(publicID).subscribe(ack => {
            this.toastService.success('Log was deleted!');
          }, (error) => {
            console.error(error);
          },
          () => {
            this.jobLogService.getJobLogs(this.taskID).subscribe((logs: ExportdLog[]) => {
              this.jobLogs = logs;
              this.existingLength = this.jobLogs.length;
              this.rerender();
            });
          }
        );
      },
      (error) => {
        console.error(error);
      });
  }

  public selectAll() {
    const table: any = $('#job-logs-datatable');
    const dataTable: any = table.DataTable();
    const rows: any = dataTable.rows();
    this.selectedObjects = [];
    if ($('.selectAll').is( ':checked' )) {
      rows.select();
      let lenx: number = rows.data().length - 1;
      while (lenx >= 0) {
        this.selectedObjects.push(rows.data()[lenx][1]);
        lenx--;
      }
    } else {
      rows.deselect();
    }
  }

  public updateDisplay(publicID: number): void {
    const index = this.selectedObjects.findIndex(d => d === publicID); // find index in your array
    if (index > -1) {
      this.selectedObjects.splice(index, 1); // remove element from array
    } else {
      this.selectedObjects.push(publicID);
    }
  }

  public delSelected() {
    if (this.selectedObjects.length > 0) {
      this.cleanupInProgress = true;
      const entriesLength = this.selectedObjects.length;
      const step = 100 / entriesLength;
      const deleteObserves: Observable<any>[] = [];
      for (const logID of this.selectedObjects) {
        deleteObserves.push(this.jobLogService.deleteLog(logID));
        this.cleanupProgress += step;
      }
      forkJoin(deleteObserves)
        .subscribe(dataArray => {this.cleanupInProgress = false;
        }, error => console.error(
          error
        ), () => {
          this.jobLogService.getJobLogs(this.taskID).subscribe((logs: ExportdLog[]) => {
            this.jobLogs = logs;
            this.selectedObjects.length = 0;
            this.existingLength = this.jobLogs.length;
            this.rerender();
          });
        });
    }
  }
  rerender(): void {
    this.dtElement.dtInstance.then((dtInstance: DataTables.Api) => {
      // Destroy the table first
      dtInstance.destroy();
      // Call the dtTrigger to rerender again
      this.dtTrigger.next();
    });
  }

  ngOnDestroy(): void {
    // Do not forget to unsubscribe the event
    this.dtTrigger.unsubscribe();
  }
}
