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

import {Component, Input } from '@angular/core';
import { FileElement } from '../../model/file-element';
import { BehaviorSubject } from 'rxjs';
import {FileService} from "../../service/file.service";
import {FileSaverService} from "ngx-filesaver";
import {RenameDialogComponent} from "../../modal/rename-dialog/rename-dialog.component";
import {FileMetadata} from "../../model/metadata";
import {NgbModal, NgbModalConfig} from "@ng-bootstrap/ng-bootstrap";

@Component({
  selector: 'cmdb-file-view-list',
  templateUrl: './file-view-list.component.html',
  styleUrls: ['./file-view-list.component.scss']
})
export class FileViewListComponent {
  private elementFiles: BehaviorSubject<FileElement[]> = new BehaviorSubject<FileElement[]>([]);

  @Input()
  set fileElements( value: BehaviorSubject<FileElement[]>) {
    this.elementFiles = value;
  }

  get fileElements(): BehaviorSubject<FileElement[]> {
    return this.elementFiles;
  }


  constructor(private fileService: FileService, private fileSaverService: FileSaverService,
              private modalService: NgbModal, private config: NgbModalConfig) {
    config.backdrop = 'static';
    config.keyboard = false;
  }

  public downloadFile(value: FileElement) {
    const {name, metadata} = value;
    this.fileService.getFileByName(name, metadata).subscribe((data: any) => {
      this.fileSaverService.save(data.body, name);
    });
  }

  public renameFile(value: any) {
    const folderModal = this.modalService.open(RenameDialogComponent);
    folderModal.componentInstance.selectedFileFolder = new BehaviorSubject<any>(value);
    folderModal.result.then((result) => {
      if (result) {
        const metadata = new FileMetadata({parent: value.public_id, folder: false });
        const fileElement = value;
        fileElement.filename = result.filename;
        this.fileService.putFile(fileElement).subscribe(() => {
          this.fileService.getAllFilesList(metadata).subscribe((data: FileElement[]) => {
            this.fileElements.next(data);
          });
        });
      }
    });
  }

  public deleteFile(value: FileElement) {
    const metadata = new FileMetadata({parent: value.public_id, folder: false });
    this.fileService.deleteFile(value.public_id, {}).subscribe(() => {
      this.fileService.getAllFilesList(metadata).subscribe((data: FileElement[]) => {
        this.fileElements.next(data);
      });
    });
  }
}
