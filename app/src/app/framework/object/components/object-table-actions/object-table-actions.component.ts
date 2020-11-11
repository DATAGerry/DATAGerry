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
* along with this program. If not, see <https://www.gnu.org/licenses/>.
*/

import { Component, EventEmitter, Input, OnDestroy, Output } from '@angular/core';
import { RenderResult } from '../../../models/cmdb-render';
import { NgbModal, NgbModalRef } from '@ng-bootstrap/ng-bootstrap';
import { ObjectPreviewModalComponent } from '../../modals/object-preview-modal/object-preview-modal.component';
import { ObjectDeleteModalComponent } from '../../modals/object-delete-modal/object-delete-modal.component';
import { ReplaySubject } from 'rxjs';

@Component({
  selector: 'cmdb-object-table-actions',
  templateUrl: './object-table-actions.component.html',
  styleUrls: ['./object-table-actions.component.scss']
})
export class ObjectTableActionsComponent implements OnDestroy {

  /**
   * Component wide un-subscriber
   * @private
   */
  private subscriber: ReplaySubject<void> = new ReplaySubject<void>();

  /**
   * Public id of the object.
   */
  @Input() public publicID: number;

  /**
   * Rendered object
   */
  @Input() public result: RenderResult;

  /**
   * Emitter when element was deleted.
   */
  @Output() public deleteEmitter: EventEmitter<number> = new EventEmitter<number>();

  private modalRef: NgbModalRef;

  constructor(private modalService: NgbModal) {
  }

  /**
   * Open the preview modal.
   */
  public openPreviewModal(): void {
    this.modalRef = this.modalService.open(ObjectPreviewModalComponent, { size: 'lg' });
    this.modalRef.componentInstance.renderResult = this.result;
  }

  /**
   * Open the delete modal.
   */
  public openDeleteModal(): void {
    this.modalRef = this.modalService.open(ObjectDeleteModalComponent, { size: 'lg' });
    this.modalRef.componentInstance.publicID = this.result.object_information.object_id;
    this.modalRef.result.then((response: any) => {
      if (!isNaN(+response)) {
        this.deleteEmitter.emit(+response);
      }
    });
  }

  public ngOnDestroy(): void {
    this.subscriber.next();
    this.subscriber.complete();
    if (this.modalRef) {
      this.modalRef.close();
    }
  }

}
