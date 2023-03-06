/*
* DATAGERRY - OpenSource Enterprise CMDB
* Copyright (C) 2023 becon GmbH
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

import {Component, OnInit} from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { FileMetadata } from '../../model/metadata';
import { FileService } from '../../service/file.service';
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';
import { FileElement } from '../../model/file-element';
import { APIGetMultiResponse } from '../../../../../services/models/api-response';
import {CollectionParameters} from "../../../../../services/models/api-parameter";

@Component({
  selector: 'cmdb-move-dialog',
  templateUrl: './move-dialog.component.html',
  styleUrls: ['./move-dialog.component.scss']
})
export class MoveDialogComponent implements OnInit {

  public basicForm: FormGroup;
  public destinationFolder: FileElement[] = [];
  private readonly defaultApiParameter: CollectionParameters = {page: 1, limit: 100, order: 1};

  constructor(private fileService: FileService, public activeModal: NgbActiveModal) {}

  groupByFn = (item) => item.metadata.parent ? item.metadata.parent : 0;

  groupValueFn = (_: string, children: any[]) => (
    {
      parentName: this.findParentName(children[0].metadata.parent),
      total: children.length,
      public_id: children[0].metadata.parent
    })

  private findParentName(publicID: number) {
    return publicID === null ? 'Without Parent' : this.destinationFolder.filter(x => x.public_id === publicID)[0].filename;
  }

  public ngOnInit(): void {
    this.basicForm = new FormGroup({
      folder: new FormControl(null, Validators.required)
    });

    this.fileService.getAllFilesList(new FileMetadata({folder: true}), this.defaultApiParameter)
      .subscribe( (data: APIGetMultiResponse<FileElement>) => {
        this.destinationFolder = data.results;
    });
  }
}
