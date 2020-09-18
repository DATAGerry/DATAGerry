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

import { Component, EventEmitter, Input, OnChanges, OnInit, Output, SimpleChanges } from '@angular/core';
import { FileService } from '../../service/file.service';
import { FileElement } from '../../model/file-element';
import { FileMetadata } from '../../model/metadata';
import { BehaviorSubject } from 'rxjs';

@Component({
  selector: 'cmdb-folder-tree',
  templateUrl: './folder-tree.component.html',
  styleUrls: ['./folder-tree.component.scss']
})
export class FolderTreeComponent implements OnInit, OnChanges {

  private elementFiles: any;
  private elementFileTree: FileElement[] = [];
  private metadata: FileMetadata = new FileMetadata();
  private selectedFileElement: any;

  @Input()
  set fileTree(value: FileElement[]) {
    this.elementFileTree = value;
  }

  get fileTree(): FileElement[] {
    return this.elementFileTree;
  }

  @Input()
  set fileElements(value: BehaviorSubject<FileElement[]>) {
    this.elementFiles = value;
  }

  get fileElements(): BehaviorSubject<FileElement[]> {
    return this.elementFiles;
  }

  @Input()
  set selectedFileFolder( value: BehaviorSubject<any>) {
    this.selectedFileElement = value;
  }

  get selectedFileFolder(): BehaviorSubject<any> {
    return this.selectedFileElement;
  }

  /**
   * Marks a property in a child component as a
   * doorway through which data can travel from the child to the parent.
   */
  @Output() createFileElementEvent = new EventEmitter<any>();
  @Output() renameFileElementEvent = new EventEmitter<any>();
  @Output() deleteFileElementEvent = new EventEmitter<any>();

  constructor(private fileService: FileService) { }

  static createFolderTree(arr): any[] {
    const tree = [];
    const mappedArr = {};
    let arrElem;
    let mappedElem;

    // First map the nodes of the array to an object -> create a hash table.
    for (let i = 0, len = arr.length; i < len; i++) {
      arrElem = arr[i];
      mappedArr[arrElem.public_id] = arrElem;
      mappedArr[arrElem.public_id].children = [];
    }

    for (const id in mappedArr) {
      if (mappedArr.hasOwnProperty(id)) {
        mappedElem = mappedArr[id];
        // If the element is not at the root level, add it to its parent array of children.
        if (mappedElem.metadata.parent) {
          mappedArr[mappedElem.metadata.parent].children.push(mappedElem);
        } else {
          tree.push(mappedElem);
        }
      }
    }
    return [{name: 'root', hasSubFolders: true, children: tree, metadata: { parent: null } }];
  }

  ngOnInit(): void {
    this.getTreeList();
  }

  ngOnChanges(changes: SimpleChanges): void {
    this.getTreeList();
  }

  private getTreeList() {
    this.metadata.folder = true;
    this.fileService.getAllFilesList(this.metadata).subscribe((data: FileElement[]) => {
      this.fileTree = FolderTreeComponent.createFolderTree(data);
    });
  }

  public dropTree(event, value): void {
    this.selectedFileFolder.next(value);
    value.hasSubFolders = !value.hasSubFolders;
    event.stopPropagation();
  }

  public loadFolderFiles(value) {
    this.selectedFileFolder.next(value);
    if (value) {
      const metadata = new FileMetadata({parent: value.public_id, folder: false });
      this.fileService.getAllFilesList(metadata).subscribe((data: FileElement[]) => {
        this.fileElements.next(data);
      });
    }
  }

  public createFolder(): void {
    this.createFileElementEvent.emit(this.selectedFileFolder);
  }

  public renameFolder(): void {
    this.renameFileElementEvent.emit();
  }

  public deleteFolder(value: FileElement): void {
    this.deleteFileElementEvent.emit(value);
  }

  public loadContextMenu() {
    console.log('loadContextMenu');
  }
}
