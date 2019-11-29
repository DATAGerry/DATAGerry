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

import {Component, Input, OnInit, ViewChild} from '@angular/core';
import { ExportdJobLogService } from '../../services/exportd-job-log.service';
import { ActivatedRoute } from '@angular/router';
import {NgbActiveModal, NgbModal} from '@ng-bootstrap/ng-bootstrap';
import { ToastService } from '../../../layout/toast/toast.service';
import { ExecuteState } from '../../models/modes_job.enum';
import { ExportdLog } from '../../models/exportd-log';
import {CmdbLog} from "../../../framework/models/cmdb-log";
import {forkJoin, Observable} from "rxjs";
import {DeleteModalComponent} from "../log-object-settings/log-object-settings.component";

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
export class DeleteExportdModalComponent {
  @Input() publicID: number;

  constructor(public activeModal: NgbActiveModal) {
  }
}

@Component({
  selector: 'cmdb-log-exportd-settings',
  templateUrl: './log-exportd-settings.component.html',
  styleUrls: ['./log-exportd-settings.component.scss']
})
export class LogExportdSettingsComponent implements OnInit {

  public activeLogList: ExportdLog[] = [];
  public activeLength: number = 0;
  public deActiveLogList: ExportdLog[];
  public deActiveLength: number = 0;
  public deleteLogList: ExportdLog[];
  public deleteLogLength: number = 0;
  public cleanupInProgress: boolean = false;
  public cleanupProgress: number = 0;
  public existingLength: number = 0;
  public modes = ExecuteState;

  constructor( private exportdLogService: ExportdJobLogService, private route: ActivatedRoute,
               private modalService: NgbModal, private toastService: ToastService) {
  }

  public ngOnInit(): void {
    this.reloadLogs();
  }

  private reloadLogs() {
    this.loadExists();
    this.loadNotExists();
  }

  private loadExists() {
    this.exportdLogService.getLogsWithExistingObject().subscribe((activeLogs: ExportdLog[]) => {
      this.activeLogList = activeLogs;
    }, error => {
      console.error(error);
      this.activeLength = 0;
    }, () => {
      this.activeLength = this.activeLogList.length;
    });
  }

  private loadNotExists() {
    this.exportdLogService.getLogsWithNotExistingObject().subscribe((deActiveLogs: ExportdLog[]) => {
      this.deActiveLogList = deActiveLogs;
    }, error => {
      console.error(error);
      this.deActiveLength = 0;
    }, () => {
      this.deActiveLength = this.deActiveLogList.length;
    });
  }

  public deleteLog(publicID: number, reloadList: string) {
    const deleteModalRef = this.modalService.open(DeleteModalComponent);
    deleteModalRef.componentInstance.publicID = publicID;
    deleteModalRef.result.then(result => {
        this.exportdLogService.deleteLog(result).subscribe(ack => {
            this.toastService.show('Log was deleted!');
          }, (error) => {
            console.error(error);
          },
          () => {
            switch (reloadList) {
              case 'active':
                this.loadExists();
                break;
              case 'deactive':
                this.loadNotExists();
                break;
            }
          }
        );
      },
      (error) => {
        console.error(error);
      });
  }

  public cleanup(publicIDs: number[], reloadList: string) {
    this.cleanupInProgress = true;
    const entriesLength = publicIDs.length;
    const step = 100 / entriesLength;
    const deleteObserves: Observable<any>[] = [];
    for (const logID of publicIDs) {
      deleteObserves.push(this.exportdLogService.deleteLog(logID));
      this.cleanupProgress += step;
    }
    forkJoin(deleteObserves)
      .subscribe(dataArray => {
        this.cleanupInProgress = false;
      }, error => console.error(
        error
      ), () => {
        switch (reloadList) {
          case 'active':
            this.loadExists();
            break;
          case 'deactive':
            this.loadNotExists();
            break;
        }
      });

  }
}
