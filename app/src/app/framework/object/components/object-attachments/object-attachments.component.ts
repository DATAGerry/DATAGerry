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

import { Component, OnDestroy, OnInit } from '@angular/core';
import { FileSaverService } from 'ngx-filesaver';
import { FileService } from '../../../../filemanager/service/file.service';
import { FileMetadata } from '../../../../filemanager/model/metadata';
import { ActivatedRoute } from '@angular/router';
import { NgbModal, NgbModalConfig, NgbModalRef } from '@ng-bootstrap/ng-bootstrap';
import { AddAttachmentsModalComponent } from '../../../../layout/helpers/modals/add-attachments-modal/add-attachments-modal.component';
import { APIGetMultiResponse } from '../../../../services/models/api-response';
import { FileElement } from '../../../../filemanager/model/file-element';

@Component({
  selector: 'cmdb-object-attachments',
  templateUrl: './object-attachments.component.html',
  styleUrls: ['./object-attachments.component.scss']
})
export class ObjectAttachmentsComponent implements OnInit, OnDestroy {

  public attachmentsTotal: number = 0;
  private metadata: FileMetadata = new FileMetadata();
  private modalRef: NgbModalRef;

  constructor(private fileService: FileService, private fileSaverService: FileSaverService,
              private route: ActivatedRoute, private modalService: NgbModal, private config: NgbModalConfig) {
    this.route.params.subscribe((params) => {
      this.metadata.reference = Number(params.publicID);
      this.metadata.reference_type = 'object';
    });
    config.backdrop = 'static';
    config.keyboard = false;
  }

  public ngOnInit(): void {
    this.fileService.getAllFilesList(this.metadata).subscribe((resp: APIGetMultiResponse<FileElement>) => {
      this.attachmentsTotal = resp.total;
    });
  }

  public ngOnDestroy(): void {
    if (this.modalRef) {
      this.modalRef.close();
    }
  }

  public addAttachments() {
    this.modalRef = this.modalService.open(AddAttachmentsModalComponent);
    this.modalRef.componentInstance.metadata = this.metadata;
    this.modalRef.result.then((result) => {
      this.attachmentsTotal = result.total;
    });
  }
}
