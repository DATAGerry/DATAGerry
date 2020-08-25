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


import { Component, EventEmitter, Input, OnDestroy, OnInit, Output} from '@angular/core';
import { TableColumnAction } from '../../../models/table-columns-action';
import { RenderResult } from '../../../../../../framework/models/cmdb-render';
import { CmdbMode } from '../../../../../../framework/modes.enum';
import { NgbActiveModal, NgbModal, NgbModalRef } from '@ng-bootstrap/ng-bootstrap';
import { ObjectPreviewModalComponent } from '../../../../../../framework/object/modals/object-preview-modal/object-preview-modal.component';
import { ObjectService } from '../../../../../../framework/services/object.service';

@Component({
  selector: 'cmdb-action-preview',
  templateUrl: './action-preview.component.html',
  styleUrls: ['./action-preview.component.scss']
})
export class ActionPreviewComponent implements  OnDestroy {

  @Input() data: TableColumnAction[];
  @Input() publicID: number;
  public mode = CmdbMode.View;
  public refObject: RenderResult;
  private modalRef: NgbModalRef;

  constructor(public activeModal: NgbActiveModal, private modalService: NgbModal, public objectService: ObjectService) {
  }

  public ngOnDestroy(): void {
    if (this.modalRef) {
      this.modalRef.close();
    }
  }

  preview() {
    this.objectService.getObject(this.publicID).subscribe(resp => {
      this.modalRef = this.modalService.open(ObjectPreviewModalComponent, { size: 'lg' });
      this.modalRef.componentInstance.renderResult = resp;
    });
  }
}
