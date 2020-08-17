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

import { Component, EventEmitter, OnInit, Output } from '@angular/core';
import { FileService } from './service/file.service';
import { NgbModal, NgbModalConfig } from '@ng-bootstrap/ng-bootstrap';
import { NewFolderDialogComponent } from './modal/new-folder-dialog/new-folder-dialog.component';
import { BehaviorSubject } from 'rxjs';

@Component({
  selector: 'cmdb-file-manager',
  templateUrl: './file-manager.component.html',
  styleUrls: ['./file-manager.component.scss']
})
export class FileManagerComponent implements OnInit {

  @Output() folderAdded = new EventEmitter<{ name: string }>();
  public  selectedFileElement = new BehaviorSubject<any>(null);

  constructor(private fileService: FileService, private modalService: NgbModal, private config: NgbModalConfig) {
    config.backdrop = 'static';
    config.keyboard = false;
  }

  ngOnInit() {
  }

  public addFolder() {
    const folderModal = this.modalService.open(NewFolderDialogComponent);
    folderModal.componentInstance.selectedFileElement = this.selectedFileElement;

  }
}
