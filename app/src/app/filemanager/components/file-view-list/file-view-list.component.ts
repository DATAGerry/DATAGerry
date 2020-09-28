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

import { Component, Directive, EventEmitter, HostListener, Input, Output } from '@angular/core';
import { FileElement } from '../../model/file-element';
import { BehaviorSubject } from 'rxjs';
import { FileService } from '../../service/file.service';
import { FileSaverService } from 'ngx-filesaver';
import { RenameDialogComponent} from '../../modal/rename-dialog/rename-dialog.component';
import { NgbModal, NgbModalConfig } from '@ng-bootstrap/ng-bootstrap';
import { MoveDialogComponent } from '../../modal/move-dialog/move-dialog.component';
import { CollectionParameters } from '../../../services/models/api-parameter';
import { InfiniteScrollService } from '../../../layout/services/infinite-scroll.service';

enum SortType {
  TYPE = 'metadata.mime_type',
  SIZE = 'length',
  AUTHOR = 'metadata.author_id',
  FILENAME = 'filename'
}

@Directive({
  selector: '[tableSortEvent]'
})
export class TableEventDirective {

  constructor( private scrollService: InfiniteScrollService) {
  }

  @Output() valueChanged = new EventEmitter<any>();

  public htmlElement: HTMLElement;
  private readonly tag: string = 'viewScroll';

  @HostListener('click', ['$event'])
  onClickHandler(event: MouseEvent) {
    document.getElementById('file-view-list').scrollTop = 0;
    this.htmlElement = (event.target as HTMLElement);
    this.removeActiveClass();
    this.setSortDirection();
  }

  private removeActiveClass(): void {
    const children = this.htmlElement.parentNode.children;
    let count = children.length;
    while (count--) { children[count].classList.remove('active'); }
  }

  private setSortDirection(): void {
    if (this.htmlElement.classList.contains('_desc')) {
      this.htmlElement.classList.remove('_desc');
      this.htmlElement.classList.add('_asc');
    } else {
      this.htmlElement.classList.remove('_asc');
      this.htmlElement.classList.add('_desc');
    }
    this.htmlElement.classList.add('active');
    this.reloadApiParameters();
  }

  private reloadApiParameters() {
    this.scrollService.setCollectionParameters(
      1,
      100,
      (SortType)[this.htmlElement.innerText.toUpperCase()],
      this.htmlElement.classList.contains('_desc') ? -1 : 1,
      this.tag);
    this.valueChanged.emit(this.scrollService.getCollectionParameters(this.tag));
  }
}

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

  @Output() loadFileElementEvent = new EventEmitter<any>();

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
        const fileElement = value;
        fileElement.filename = result.filename;
        this.postFileChanges(fileElement);
      }
    });
  }

  public moveFile(value: any) {
    const folderModal = this.modalService.open(MoveDialogComponent);
    folderModal.result.then((result) => {
      if (result) {
        const fileElement = value;
        fileElement.filename = value.name;
        fileElement.metadata.parent = result.parent;
        this.postFileChanges(fileElement);
      }
    });
  }

  public deleteFile(value: FileElement) {
    this.fileService.deleteFile(value.public_id, {}).subscribe(() => {
      this.loadFolderFiles();
    });
  }

  private postFileChanges(curr: any): void {
    this.fileService.putFile(curr).subscribe(() => {
      this.loadFolderFiles();
    });
  }

  public loadFolderFiles(value?: CollectionParameters) {
    this.loadFileElementEvent.emit(value);
  }
}
