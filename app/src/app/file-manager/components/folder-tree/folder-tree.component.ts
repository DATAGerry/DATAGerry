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

import {Component, Input, OnInit} from '@angular/core';
import { FileService } from '../../service/file.service';
import { FileElement } from '../../model/file-element';
import { FileMetadata } from '../../model/metadata';

@Component({
  selector: 'cmdb-folder-tree',
  templateUrl: './folder-tree.component.html',
  styleUrls: ['./folder-tree.component.scss']
})
export class FolderTreeComponent implements OnInit {

  @Input()
  set selectedFileFolder( value: any) {
    this.selectedFileElement = value;
  }

  get selectedFileFolder(): any {
    return this.selectedFileElement;
  }
  constructor(private fileService: FileService) { }

  private metadata: FileMetadata = new FileMetadata();
  public fileTree: FileElement[];
  private selectedFileElement: any;

  // For testing
  public list = [
    {name: 'top', children: [
        {name: 'level1', children: [
            {name: 'level2'}
          ]}
      ]}
  ];

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
    return tree;
  }

  ngOnInit() {
    this.metadata.folder = true;
    this.fileService.getAllFilesList(this.metadata).subscribe((data: FileElement[]) => {
      this.fileTree = FolderTreeComponent.createFolderTree(data);
    });
  }

  public listClick(event, newValue): void {
    this.selectedFileFolder.next(newValue);
    newValue.hasSubFolders = !newValue.hasSubFolders;
    event.stopPropagation();
  }
}
