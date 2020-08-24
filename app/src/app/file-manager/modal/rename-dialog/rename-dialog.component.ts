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
import { BehaviorSubject } from 'rxjs';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { FileMetadata } from '../../model/metadata';
import { checkFolderExistsValidator, FileService } from '../../service/file.service';
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';
import { ToastService } from '../../../layout/toast/toast.service';

@Component({
  selector: 'cmdb-rename-dialog',
  templateUrl: './rename-dialog.component.html',
  styleUrls: ['./rename-dialog.component.scss']
})
export class RenameDialogComponent implements OnInit {

  private selectedFileElement: BehaviorSubject<any>;

  @Input()
  set selectedFileFolder( value: BehaviorSubject<any>) {
    this.selectedFileElement = value;
  }

  get selectedFileFolder(): BehaviorSubject<any> {
    return this.selectedFileElement;
  }
  public basicForm: FormGroup;


  static generateMetaData(value: BehaviorSubject<any> ): FileMetadata {
    const fileElement = value.getValue();
    return new FileMetadata(
      {folder: fileElement == null ? false : fileElement.metadata.folder,
          parent: fileElement == null ? null : fileElement.public_id }
    );
  }

  constructor(private fileService: FileService, public activeModal: NgbActiveModal, private toast: ToastService) {}

  public ngOnInit(): void {
    this.basicForm = new FormGroup({
      name: new FormControl('', Validators.required)
    });
    this.basicForm.get('name').setAsyncValidators(checkFolderExistsValidator(this.fileService,
      RenameDialogComponent.generateMetaData(this.selectedFileFolder)));
  }

  public get name() {
    return this.basicForm.get('name');
  }

}
