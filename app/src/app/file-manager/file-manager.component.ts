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
import { FileService } from './service/file.service';
import {NgbModal, NgbModalConfig, NgbModalRef} from '@ng-bootstrap/ng-bootstrap';
import { NewFolderDialogComponent } from './modal/new-folder-dialog/new-folder-dialog.component';
import { BehaviorSubject } from 'rxjs';
import { FileElement } from './model/file-element';
import { FileMetadata } from './model/metadata';
import { AddAttachmentsModalComponent } from '../layout/helpers/modals/add-attachments-modal/add-attachments-modal.component';
import { GeneralModalComponent } from '../layout/helpers/modals/general-modal/general-modal.component';
import { RenameDialogComponent } from './modal/rename-dialog/rename-dialog.component';

@Component({
  selector: 'cmdb-file-manager',
  templateUrl: './file-manager.component.html',
  styleUrls: ['./file-manager.component.scss']
})
export class FileManagerComponent implements OnInit {

  /**
   * Data sharing between components
   */
  public fileElements = new BehaviorSubject<FileElement[]>([]);
  public fileTree: FileElement[] = [];
  public selectedFolderElement = new BehaviorSubject<any>(null);

  /**
   * Metadata for filtering Files from Database
   */
  private metadata: FileMetadata = new FileMetadata({folder: false});
  private modalRef: NgbModalRef;

  constructor(private fileService: FileService, private modalService: NgbModal, private config: NgbModalConfig) {
    config.backdrop = 'static';
    config.keyboard = false;
  }

  ngOnInit() {
    this.loadFiles(this.metadata);
  }

  private loadFiles(metadata: FileMetadata): void {
    this.fileService.getAllFilesList(metadata).subscribe((data: any) => {
      this.fileElements.next(data);
    });
  }

  private generateMetadata(): FileMetadata {
    const folder = this.selectedFolderElement;
    return new FileMetadata(
      {folder: false, ...{ parent: folder.getValue() == null ? null : folder.getValue().public_id }}
    );
  }

  public addFolder() {
    this.modalRef = this.modalService.open(NewFolderDialogComponent);
    this.modalRef.componentInstance.selectedFileFolder = this.selectedFolderElement;
    this.modalRef.result.then((result) => {
      this.fileTree = result.fileTree;
    });
  }

  public uploadFile() {
    const metadata = this.generateMetadata();
    this.modalRef = this.modalService.open(AddAttachmentsModalComponent);
    this.modalRef.componentInstance.metadata = metadata;
    this.modalRef.result.then(() => {
      this.fileService.getAllFilesList(metadata).subscribe((data: any) => {
        this.fileElements.next(data);
      });
    });
  }

  public renameFile() {
    this.modalRef = this.modalService.open(RenameDialogComponent);
    this.modalRef.componentInstance.selectedFileFolder = this.selectedFolderElement;
    this.modalRef.result.then((result) => {
      if (result) {
        const fileElement = this.selectedFolderElement.getValue();
        fileElement.filename = result.filename;
        this.fileService.putFile(fileElement).subscribe(() => {
          this.fileService.getAllFilesList({folder: true}).subscribe((data: FileElement[]) => {
            this.fileTree = data;
          });
        });
      }
    });
  }

  public deleteFiles(value: FileElement) {
    this.selectedFolderElement.next(value);
    const metadata = this.generateMetadata();
    this.deleteFileModal(value.name).then(result => {
      if (result) {
        this.fileService.deleteFile(value.public_id, metadata).subscribe(() => {
            this.fileService.getAllFilesList({folder: true}).subscribe((data: FileElement[]) => {
              this.fileTree = data;
            });
          }
        );
      }
    });
  }

  private deleteFileModal(filename: string) {
    this.modalRef = this.modalService.open(GeneralModalComponent);
    this.modalRef.componentInstance.title = `Delete ${filename}`;
    this.modalRef.componentInstance.modalMessage =
      `Are you sure you want to delete ${filename} Folder?`;
    this.modalRef.componentInstance.subModalMessage =
      `All files associated to this Folder will permanently deleted. This operation can not be undone!`;
    this.modalRef.componentInstance.buttonDeny = 'Cancel';
    this.modalRef.componentInstance.buttonAccept = 'Delete';
    return this.modalRef.result;
  }
}
