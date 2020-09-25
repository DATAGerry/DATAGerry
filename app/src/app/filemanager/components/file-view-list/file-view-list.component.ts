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

import { Component, Input } from '@angular/core';
import { FileElement } from '../../model/file-element';
import { BehaviorSubject } from 'rxjs';
import { FileService } from '../../service/file.service';
import { FileSaverService } from 'ngx-filesaver';
import { RenameDialogComponent} from '../../modal/rename-dialog/rename-dialog.component';
import { FileMetadata } from '../../model/metadata';
import { NgbModal, NgbModalConfig } from '@ng-bootstrap/ng-bootstrap';
import { MoveDialogComponent } from '../../modal/move-dialog/move-dialog.component';
import { APIGetMultiResponse } from '../../../services/models/api-response';

@Component({
  selector: 'cmdb-file-view-list',
  templateUrl: './file-view-list.component.html',
  styleUrls: ['./file-view-list.component.scss']
})
export class FileViewListComponent {

  private elementFiles: FileElement[] = [];

  @Input()
  set fileElements( value: FileElement[]) {
    this.elementFiles = value;
  }

  get fileElements(): FileElement[] {
    return this.elementFiles;
  }

  constructor(public fileService: FileService, private fileSaverService: FileSaverService,
              private modalService: NgbModal, private config: NgbModalConfig) {
    config.backdrop = 'static';
    config.keyboard = false;
  }

  public downloadFile(value: FileElement) {
    const {name, metadata} = value;
    this.fileService.downloadFile(name, metadata).subscribe((data: any) => {
      this.fileSaverService.save(data.body, name);
    });
  }

  public renameFile(value: any) {
    const folderModal = this.modalService.open(RenameDialogComponent);
    folderModal.componentInstance.selectedFileFolder = new BehaviorSubject<any>(value);
    folderModal.result.then((result) => {
      if (result) {
        const metadata = new FileMetadata({parent: value.metadata.parent, folder: false });
        const fileElement = value;
        fileElement.filename = result.filename;
        this.postFileChanges(fileElement, metadata);
      }
    });
  }

  public moveFile(value: any) {
    const folderModal = this.modalService.open(MoveDialogComponent);
    folderModal.result.then((result) => {
      if (result) {
        const metadata = new FileMetadata({parent: value.metadata.parent, folder: false });
        const fileElement = value;
        fileElement.filename = value.name;
        fileElement.metadata.parent = result.parent;
        this.postFileChanges(fileElement, metadata);
      }
    });
  }

  public deleteFile(value: FileElement) {
    const metadata = new FileMetadata({parent: value.metadata.parent, folder: false });
    this.fileService.deleteFile(value.public_id, {}).subscribe(() => {
      this.fileService.getAllFilesList(metadata).subscribe((data: APIGetMultiResponse<FileElement>) => {
        this.fileElements = data.results;
      });
    });
  }

  private postFileChanges(curr: any, metadata: any): void {
    this.fileService.putFile(curr).subscribe(() => {
      this.fileService.getAllFilesList(metadata).subscribe((data: APIGetMultiResponse<FileElement>) => {
        this.fileElements = data.results;
      });
    });
  }
}
