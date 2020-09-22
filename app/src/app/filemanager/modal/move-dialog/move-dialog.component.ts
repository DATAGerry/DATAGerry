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

import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { FileMetadata } from '../../model/metadata';
import { FileService } from '../../service/file.service';
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';
import { ToastService } from '../../../layout/toast/toast.service';
import { FileElement } from '../../model/file-element';

@Component({
  selector: 'cmdb-move-dialog',
  templateUrl: './move-dialog.component.html',
  styleUrls: ['./move-dialog.component.scss']
})
export class MoveDialogComponent implements OnInit {

  public basicForm: FormGroup;
  public destinationFolder: FileElement[] = [];

  constructor(private fileService: FileService, public activeModal: NgbActiveModal) {}

  public ngOnInit(): void {
    this.basicForm = new FormGroup({
      folder: new FormControl(null, Validators.required)
    });
    this.fileService.getAllFilesList(new FileMetadata({folder: true})).subscribe( (data: any) => {
      this.destinationFolder = data.results;
      this.destinationFolder.push(new FileElement({name: '/', public_id: null, metadata: { parent: null } }));
    });
  }
}
