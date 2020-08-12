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

@Component({
  selector: 'cmdb-new-folder-dialog',
  templateUrl: './new-folder-dialog.component.html',
  styleUrls: ['./new-folder-dialog.component.scss']
})
export class NewFolderDialogComponent implements OnInit {

  @Input() selectedFileElement: BehaviorSubject<any>;
  public basicForm: FormGroup;

  constructor(private fileService: FileService, public activeModal: NgbActiveModal, private toast: ToastService) {}

  public ngOnInit(): void {
    this.basicForm = new FormGroup({
      name: new FormControl('', Validators.required)
    });
    this.basicForm.get('name').setAsyncValidators(checkFolderExistsValidator(this.fileService));
  }

  public get name() {
    return this.basicForm.get('name');
  }

  public createFolder(): void {
    const metadata: FileMetadata = new FileMetadata({folder: true});
    const folder = new File(['folder'], this.name.value, {
      type: 'application/json',
    });
    console.log(this.selectedFileElement.getValue());
    // this.fileService.postFile( folder, metadata).subscribe(() => {
    //   this.toast.show(`Folder was successfully created: ${this.name.value}`);
    //   this.activeModal.close();
    // });
  }
}
