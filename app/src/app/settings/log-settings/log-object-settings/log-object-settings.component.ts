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

* You should have received a copy of the GNU Affero General Public License
* along with this program.  If not, see <https://www.gnu.org/licenses/>.
*/

import { Component, Input, Output, EventEmitter} from '@angular/core';
import { LogService } from '../../../framework/services/log.service';
import { CmdbLog } from '../../../framework/models/cmdb-log';
import { NgbActiveModal, NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { ToastService } from '../../../layout/toast/toast.service';
import { Observable, forkJoin, ReplaySubject } from 'rxjs';
import { takeUntil } from 'rxjs/operators';

@Component({
  selector: 'cmdb-modal-content',
  template: `
      <div class="modal-header">
          <h4 class="modal-title" id="modal-basic-title">Delete Log</h4>
          <button type="button" class="close" aria-label="Close" (click)=" handleModalDismiss()">
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
  @Output() isDismissClicked = new EventEmitter <boolean> ();

  constructor(public activeModal: NgbActiveModal) {
  }

  handleModalDismiss() {
    this.activeModal.dismiss('Cross click')
    this.isDismissClicked.emit(true)
  }
}


@Component({
  selector: 'cmdb-log-object-settings',
  templateUrl: './log-object-settings.component.html',
  styleUrls: ['./log-object-settings.component.scss']
})
export class LogObjectSettingsComponent {

  public activeLogList: CmdbLog[];
  public reloadActiveLogs: boolean = false;
  public deActiveLogList: CmdbLog[];
  public reloadDeActiveLogs: boolean = false;
  public deActiveLength: number = 0;
  public deleteLogList: CmdbLog[];
  public reloadDeleteLogs: boolean = false;
  public deleteLogLength: number = 0;
  public cleanupInProgress: boolean = false;
  public cleanupProgress: number = 0;
  isDismissClicked: boolean = false;

  /**
   * Component un-subscriber.
   */
  private subscriber: ReplaySubject<void> = new ReplaySubject<void>();

  constructor(private logService: LogService, private modalService: NgbModal, private toastService: ToastService) {
  }


  public deleteLog(publicID: number, reloadList: string) {
    const deleteModalRef = this.modalService.open(DeleteModalComponent);
    deleteModalRef.componentInstance.publicID = publicID;
    deleteModalRef.componentInstance.isDismissClicked.subscribe((dismissed: boolean) => {
    this.isDismissClicked = dismissed
    });
    deleteModalRef.result.then(result => {
        this.logService.deleteLog(result).pipe(takeUntil(this.subscriber)).subscribe(() => {
            this.toastService.success('Log was deleted!');
          }, (error) => {
            console.error(error);
          },
          () => {
            switch (reloadList) {
              case 'active':
                this.reloadActiveLogs = true;
                break;
              case 'deactive':
                this.reloadDeActiveLogs = true;
                break;
              case 'delete':
                this.reloadDeleteLogs = true;
                break;
            }
          }
        );
      },
      (error) => {
        if (!this.isDismissClicked && error !== 'Cross click') {
          console.error(error);
        }
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
      .subscribe(() => {
        this.cleanupInProgress = false;
      }, error => console.error(
        error
      ), () => {
        switch (reloadList) {
          case 'active':
            this.reloadActiveLogs = true;
            break;
          case 'deactive':
            this.reloadDeActiveLogs = true;
            break;
          case 'delete':
            this.reloadDeleteLogs = true;
            break;
        }
      });

  }
}
