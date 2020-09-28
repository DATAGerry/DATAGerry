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

import { Component, HostListener, OnDestroy, OnInit } from '@angular/core';
import { FileService } from './service/file.service';
import { NgbModal, NgbModalConfig, NgbModalRef } from '@ng-bootstrap/ng-bootstrap';
import { NewFolderDialogComponent } from './modal/new-folder-dialog/new-folder-dialog.component';
import { BehaviorSubject } from 'rxjs';
import { FileElement } from './model/file-element';
import { FileMetadata } from './model/metadata';
import { AddAttachmentsModalComponent } from '../layout/helpers/modals/add-attachments-modal/add-attachments-modal.component';
import { GeneralModalComponent } from '../layout/helpers/modals/general-modal/general-modal.component';
import { RenameDialogComponent } from './modal/rename-dialog/rename-dialog.component';
import { MoveDialogComponent } from './modal/move-dialog/move-dialog.component';
import { InfiniteScrollService } from '../layout/services/infinite-scroll.service';
import { CollectionParameters } from '../services/models/api-parameter';
import { APIGetMultiResponse } from '../services/models/api-response';

@Component({
  selector: 'cmdb-filemanager',
  templateUrl: './filemanager.component.html',
  styleUrls: ['./filemanager.component.scss']
})
export class FilemanagerComponent implements OnInit, OnDestroy {

  constructor(private fileService: FileService, private modalService: NgbModal, private config: NgbModalConfig,
              private scrollService: InfiniteScrollService) {
    config.backdrop = 'static';
    config.keyboard = false;
  }

  /**
   * Data sharing between components
   */
  public fileElements: FileElement[] = [];
  public fileTree: FileElement[] = [];
  public selectedFolderElement = new BehaviorSubject<any>(null);

  /**
   * Metadata for filtering Files from Database
   */
  private apiParameter: CollectionParameters = {page: 1, limit: 100, sort: 'filename', order: -1};
  private metadata: FileMetadata = new FileMetadata({folder: false});
  private modalRef: NgbModalRef;

  /**
   * Detecting scroll direction
   */
  private page: number;
  private lastPage: number;
  private readonly tag: string = 'viewScroll';

  @HostListener('scroll', ['$event']) onScrollHost(e: Event): void {
    if (this.scrollService.bottomReached(e, this.tag) && this.page <= this.lastPage) {
      this.loadFiles(this.scrollService.getCollectionParameters(this.tag), true);
    }
  }

  ngOnInit() {
    this.loadFiles(this.apiParameter);
    this.loadFileTree();
  }

  /**
   * Get all attachments as a list
   * As you scroll, new records are added to the attachments.
   * Without the scrolling parameter the attachments are reinitialized
   * @param apiParameters Instance of {@link CollectionParameters}
   * @param onScroll Control if it is a new file upload
   */
  public loadFiles(apiParameters?: CollectionParameters, onScroll: boolean = false): void {
    const metadata = this.generateMetadata();
    apiParameters = apiParameters ? apiParameters : this.apiParameter;
    this.fileService.getAllFilesList(metadata, apiParameters)
      .subscribe((data: APIGetMultiResponse<FileElement>) => {
        if (onScroll) {
          this.fileElements.push(...data.results);
        } else {
          this.fileElements =  data.results;
        }
        this.updatePagination(data, apiParameters.sort, apiParameters.order);
      });
  }

  public loadFileTree() {
    this.fileService.getAllFilesList(new FileMetadata({folder: true}))
      .subscribe((data: APIGetMultiResponse<FileElement>) => {
        this.fileTree = data.results;
      });
  }

  private updatePagination(data, sort: string = 'filename', order: number = -1) {
    this.page = data.pager.page + 1;
    this.lastPage = data.pager.total_pages;
    this.scrollService.setCollectionParameters(this.page, 100, sort, order, this.tag);
    // this.apiParameter = this.scrollService.getCollectionParameters(this.tag);
  }

  private generateMetadata(folder: boolean = false): FileMetadata {
    const value = this.selectedFolderElement.getValue();
    const {public_id} = value ? value : {public_id: null};
    return new FileMetadata(
      { parent: public_id, folder }
    );
  }

  public addFolder() {
    this.modalRef = this.modalService.open(NewFolderDialogComponent);
    this.modalRef.componentInstance.selectedFileFolder = this.selectedFolderElement;
    this.modalRef.result.then((result) => {
      if (result) {
        this.reorderFolderTree(result.data);
      }
    });
  }

  private reorderFolderTree(item: FileElement) {
    this.fileService.getAllFilesList(new FileMetadata({folder: true}))
      .subscribe((data: APIGetMultiResponse<FileElement>) => {
      for (const el of data.results) {
        if (el.public_id === item.metadata.parent) {
          el.hasSubFolders = true;
        }
        if (this.fileTree.find(f => f.public_id === el.public_id && f.hasSubFolders)) {
          el.hasSubFolders = true;
        }
      }
      this.fileTree = data.results;
    });
  }

  public uploadFile() {
    const metadata = this.generateMetadata();
    this.modalRef = this.modalService.open(AddAttachmentsModalComponent);
    this.modalRef.componentInstance.metadata = metadata;
    this.modalRef.result.then(() => {
      this.fileService.getAllFilesList(metadata).subscribe((data: APIGetMultiResponse<FileElement>) => {
        this.fileElements = data.results;
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
        this.fileService.putFile(fileElement).subscribe((resp: FileElement) => {
          this.reorderFolderTree(resp);
        });
      }
    });
  }

  public moveFile() {
    this.modalRef = this.modalService.open(MoveDialogComponent);
    this.modalRef.result.then((result) => {
      if (result) {
        const fileElement = this.selectedFolderElement.getValue();
        fileElement.filename = fileElement.name;
        fileElement.metadata.parent = result.parent;
        this.fileService.putFile(fileElement).subscribe((resp: FileElement) => {
          this.reorderFolderTree(resp);
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
            this.reorderFolderTree(value);
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

  public ngOnDestroy(): void {
    if (this.modalRef) {
      this.modalRef.close();
    }
  }

  public mockups() {
    let i = 0;
    while (i < 250) {
      const folder = new File(['folder'], `${i}_mockup.json`, {
        type: 'application/json',
      });
      const metadata: FileMetadata = new FileMetadata( {
          reference : 3242,
          reference_type : 'object',
          mime_type : 'application/json',
          folder: false,
          parent : null
        }
      );
      this.fileService.postFile( folder, metadata).subscribe((resp: FileElement) => {
        console.log(resp.public_id);
      });
      i++;
    }
  }
}
