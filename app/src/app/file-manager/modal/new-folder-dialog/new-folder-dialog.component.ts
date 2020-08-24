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
import { FileMetadata } from '../../model/metadata';
import { checkFolderExistsValidator, FileService } from '../../service/file.service';
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { ToastService } from '../../../layout/toast/toast.service';
import { BehaviorSubject } from 'rxjs';
import { FileElement } from '../../model/file-element';

@Component({
  selector: 'cmdb-new-folder-dialog',
  templateUrl: './new-folder-dialog.component.html',
  styleUrls: ['./new-folder-dialog.component.scss']
})
export class NewFolderDialogComponent implements OnInit {

  private selectedFileElement: BehaviorSubject<any>;

  @Input()
  set selectedFileFolder( value: BehaviorSubject<any>) {
    this.selectedFileElement = value;
  }

  get selectedFileFolder(): BehaviorSubject<any> {
    return this.selectedFileElement;
  }
  public basicForm: FormGroup;


  static generateMetaData(parent: BehaviorSubject<any> ): FileMetadata {
    return new FileMetadata(
      {folder: true, ...{ parent: parent.getValue() == null ? null : parent.getValue().public_id }}
    );
  }

  constructor(private fileService: FileService, public activeModal: NgbActiveModal, private toast: ToastService) {}

  public ngOnInit(): void {
    this.basicForm = new FormGroup({
      name: new FormControl('', Validators.required)
    });
    this.basicForm.get('name').setAsyncValidators(checkFolderExistsValidator(this.fileService,
      NewFolderDialogComponent.generateMetaData(this.selectedFileFolder)));
  }

  public get name() {
    return this.basicForm.get('name');
  }

  public createFolder(): void {
    const folder = new File(['folder'], this.name.value, {
      type: 'application/json',
    });
    this.fileService.postFile( folder, NewFolderDialogComponent.generateMetaData(this.selectedFileElement))
      .subscribe(() => {
        this.toast.show(`Folder was successfully created: ${this.name.value}`);
        this.reloadElementTree();
    });
  }

  public reloadElementTree() {
    this.fileService.getAllFilesList({folder: true}).subscribe((data: FileElement[]) => {
      this.activeModal.close({fileTree: data});
    });
  }
}
