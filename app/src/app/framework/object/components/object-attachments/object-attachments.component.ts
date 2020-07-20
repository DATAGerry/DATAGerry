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
import { FileSaverService } from 'ngx-filesaver';
import { FileService } from '../../../../file-manager/service/file.service';
import { FileMetadata } from "../../../../file-manager/model/metadata";

@Component({
  selector: 'cmdb-object-attachments',
  templateUrl: './object-attachments.component.html',
  styleUrls: ['./object-attachments.component.scss']
})
export class ObjectAttachmentsComponent implements OnInit {

  private metadata: FileMetadata;
  public attachments: any[] = [];

  constructor(private fileService: FileService, private fileSaverService: FileSaverService) { }

  ngOnInit() {
  }

  public downloadFile(filename: string) {
    this.fileService.getFileByName(filename).subscribe((data: any) => {
      this.fileSaverService.save(data.body, filename);
    });
  }

  public uploadFile(files: FileList) {
    if (files.length > 0) {
      Array.from(files).forEach(file => {
        this.attachments.push(file);
        this.fileService.postFile(file, this.metadata).subscribe(resp => {
          console.log(resp);
        }, (err) => console.log(err));
      });
    }
  }

}
