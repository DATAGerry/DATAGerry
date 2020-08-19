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

import { Component, OnInit } from '@angular/core';
import { FileSaverService } from 'ngx-filesaver';
import { FileService } from '../../../../file-manager/service/file.service';
import { FileMetadata } from '../../../../file-manager/model/metadata';
import { ActivatedRoute } from '@angular/router';
import { NgbModal, NgbModalConfig } from '@ng-bootstrap/ng-bootstrap';
import { FileElement } from '../../../../file-manager/model/file-element';
import { AddAttachmentsModalComponent } from '../../../../layout/helpers/modals/add-attachments-modal/add-attachments-modal.component';

@Component({
  selector: 'cmdb-object-attachments',
  templateUrl: './object-attachments.component.html',
  styleUrls: ['./object-attachments.component.scss']
})
export class ObjectAttachmentsComponent implements OnInit {

  public attachmentsTotal: number = 0;
  private metadata: FileMetadata = new FileMetadata();

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
    this.fileService.getAllFilesList(this.metadata).subscribe((resp: FileElement[]) => {
      this.attachmentsTotal = resp.length;
    });
  }

  public addAttachments() {
    const attachmentAddModal = this.modalService.open(AddAttachmentsModalComponent);
    attachmentAddModal.componentInstance.metadata = this.metadata;
    attachmentAddModal.result.then((result) => {
      this.attachmentsTotal = result.total;
    });
  }
}
