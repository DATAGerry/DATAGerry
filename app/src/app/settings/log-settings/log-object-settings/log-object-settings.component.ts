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
import { LogService } from '../../../framework/services/log.service';
import { CmdbLog } from '../../../framework/models/cmdb-log';
import { NgbActiveModal, NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { ToastService } from '../../../layout/toast/toast.service';
import { Observable, forkJoin } from 'rxjs';

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
export class DeleteModalComponent {
  @Input() publicID: number;

  constructor(public activeModal: NgbActiveModal) {
  }
}


@Component({
  selector: 'cmdb-log-object-settings',
  templateUrl: './log-object-settings.component.html',
  styleUrls: ['./log-object-settings.component.scss']
})
export class LogObjectSettingsComponent implements OnInit {

  public activeLogList: CmdbLog[];
  public activeLength: number = 0;
  public deActiveLogList: CmdbLog[];
  public deActiveLength: number = 0;
  public deleteLogList: CmdbLog[];
  public deleteLogLength: number = 0;
  public cleanupInProgress: boolean = false;
  public cleanupProgress: number = 0;

  constructor(private logService: LogService, private modalService: NgbModal, private toastService: ToastService) {

  }

  public ngOnInit(): void {
    this.reloadLogs();
  }

  private reloadLogs() {
    this.loadExists();
    this.loadNotExists();
    this.loadDeletes();
  }

  private loadExists() {
    this.logService.getLogsWithExistingObject().subscribe((activeLogs: CmdbLog[]) => {
      this.activeLogList = activeLogs;
    }, error => {
      console.error(error);
      this.activeLength = 0;
    }, () => {
      this.activeLength = this.activeLogList.length;
    });
  }

  private loadNotExists() {
    this.logService.getLogsWithNotExistingObject().subscribe((deActiveLogs: CmdbLog[]) => {
      this.deActiveLogList = deActiveLogs;
    }, error => {
      console.error(error);
      this.deActiveLength = 0;
    }, () => {
      this.deActiveLength = this.deActiveLogList.length;
    });
  }

  private loadDeletes() {
    this.logService.getDeleteLogs().subscribe((deletedLogs: CmdbLog[]) => {
      this.deleteLogList = deletedLogs;
    }, error => {
      console.error(error);
      this.deleteLogLength = 0;
    }, () => {
      this.deleteLogLength = this.deleteLogList.length;
    });
  }


  public deleteLog(publicID: number, reloadList: string) {
    const deleteModalRef = this.modalService.open(DeleteModalComponent);
    deleteModalRef.componentInstance.publicID = publicID;
    deleteModalRef.result.then(result => {
        this.logService.deleteLog(result).subscribe(ack => {
            this.toastService.info('Log was deleted!');
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
              case 'delete':
                this.loadDeletes();
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
      deleteObserves.push(this.logService.deleteLog(logID));
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
          case 'delete':
            this.loadDeletes();
            break;
        }
      });

  }
}
