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
import { FileElement } from '../../../../file-manager/model/file-element';
import { ModalComponent } from '../../../../layout/helpers/modal/modal.component';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';

@Component({
  selector: 'cmdb-object-attachments',
  templateUrl: './object-attachments.component.html',
  styleUrls: ['./object-attachments.component.scss']
})
export class ObjectAttachmentsComponent implements OnInit {

  private metadata: FileMetadata = new FileMetadata();
  public attachments: FileElement[] = [];

  constructor(private fileService: FileService, private fileSaverService: FileSaverService,
              private route: ActivatedRoute, private modalService: NgbModal) {
    this.route.params.subscribe((params) => {
      this.metadata.reference = Number(params.publicID);
      this.metadata.reference_type = 'object';
    });
  }

  ngOnInit() {
    this.getFiles();
  }

  public getFiles() {
    this.fileService.getAllFilesList(this.metadata).subscribe((resp: FileElement[]) => {
      this.attachments = resp;
    });
  }

  public downloadFile(filename: string) {
    this.fileService.getFileByName(filename, this.metadata).subscribe((data: any) => {
      this.fileSaverService.save(data.body, filename);
    });
  }

  public uploadFile(files: FileList) {
    if (files.length > 0) {
      Array.from(files).forEach((file: any) => {
        if (this.attachments.find(el => el.name === file.name)) {
          const modal = this.replaceFileModal(file.name).then(result => {
            if (result) {
              this.attachments = this.attachments.filter(el => el.name !== file.name);
              return true;
            } else { return false; }
          });
          modal.then(value => {
            if (value) { this.postFile(file); }
          });
        } else { this.postFile(file); }
      });
    }
  }

  private postFile(file: any) {
    file.inProcess = true;
    this.attachments.push(file);
    this.fileService.postFile(file, this.metadata).subscribe(resp => {
      this.getFiles();
    }, (err) => console.log(err));
  }

  public deleteFile(publicID: number) {
    this.fileService.deleteFile(publicID).subscribe(resp => this.getFiles());
  }

  private replaceFileModal(filename: string) {
    const modalComponent = this.modalService.open(ModalComponent);
    modalComponent.componentInstance.title = `Replace ${filename}`;
    modalComponent.componentInstance.modalIcon = 'question-circle';
    modalComponent.componentInstance.modalMessage = `${filename} already exists. Do you want to replace it?`;
    modalComponent.componentInstance.subModalMessage = `A file with the same name already exists on this Object.
                                                        Replace it will overwrite its current contents`;
    modalComponent.componentInstance.buttonDeny = 'Cancel';
    modalComponent.componentInstance.buttonAccept = 'Replace';
    return modalComponent.result;
  }
}
