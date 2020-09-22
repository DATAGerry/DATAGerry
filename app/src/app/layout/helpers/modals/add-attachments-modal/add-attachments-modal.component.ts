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
import { FileMetadata } from '../../../../filemanager/model/metadata';
import { FileElement } from '../../../../filemanager/model/file-element';
import { FileService } from '../../../../filemanager/service/file.service';
import { FileSaverService } from 'ngx-filesaver';
import { NgbActiveModal, NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { ToastService } from '../../../toast/toast.service';
import { GeneralModalComponent } from '../general-modal/general-modal.component';

@Component({
  selector: 'cmdb-add-attachments-modal',
  templateUrl: './add-attachments-modal.component.html',
  styleUrls: ['./add-attachments-modal.component.scss']
})
export class AddAttachmentsModalComponent implements OnInit {

  @Input() metadata: FileMetadata = new FileMetadata();
  public inProcess: boolean = false;
  public attachments: FileElement[] = [];
  private dataMaxSize: number = 1024 * 1024 * 50;

  constructor(private fileService: FileService, private fileSaverService: FileSaverService,
              private modalService: NgbModal, public activeModal: NgbActiveModal, private toast: ToastService) { }

  public ngOnInit(): void {
    this.fileService.getAllFilesList(this.metadata).subscribe((resp: any) => {
      this.attachments = resp.results;
    });
  }

  public getFiles() {
    this.fileService.getAllFilesList(this.metadata).subscribe((resp: any) => {
      this.attachments = resp.results;
      this.inProcess = false;
    });
  }

  public downloadFile(filename: string) {
    this.fileService.downloadFile(filename, this.metadata).subscribe((data: any) => {
      this.fileSaverService.save(data.body, filename);
    });
  }

  public uploadFile(files: FileList) {
    if (files.length > 0) {
      Array.from(files).forEach((file: any) => {
        if (this.checkFileSizeAllow(file)) {
          if (this.attachments.find(el => el.name === file.name)) {
            const promiseModal = this.replaceFileModal(file.name).then(result => {
              if (result) {
                this.attachments = this.attachments.filter(el => el.name !== file.name);
                return true;
              } else {return false; }
            });
            promiseModal.then(value => {
              if (value) {this.postFile(file); }
            });
          } else { this.postFile(file); }
        }
      });
    }
  }

  /**
   * Check if the upload file is larger than 50 M/Bytes.
   *
   * @param file: File to be uploaded
   * @return boolean: false if larger than 50 M/Bytes, else true
   */
  private checkFileSizeAllow(file: File): boolean {
    const maxSize = this.dataMaxSize;
    if ( file.size > maxSize ) {
      this.toast.error(`File size is more then 50 M/Bytes.`);
      return false;
    }
    return true;
  }

  private postFile(file: any) {
    console.log(file);
    file.inProcess = true;
    this.inProcess = true;
    this.attachments.push(file);
    this.fileService.postFile(file, this.metadata).subscribe(() => {
      this.getFiles();
    }, (err) => console.log(err));
  }

  public deleteFile(publicID: number) {
    this.fileService.deleteFile(publicID, {}).subscribe(() => this.getFiles());
  }

  private replaceFileModal(filename: string) {
    const modalComponent = this.modalService.open(GeneralModalComponent);
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
