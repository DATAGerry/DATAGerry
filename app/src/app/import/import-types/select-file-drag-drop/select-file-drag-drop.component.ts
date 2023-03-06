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

import { Component, Input, OnInit } from '@angular/core';
import { FormGroup} from '@angular/forms';

@Component({
  selector: 'cmdb-select-file-drag-drop',
  templateUrl: './select-file-drag-drop.component.html',
  styleUrls: ['./select-file-drag-drop.component.scss']
})
export class SelectFileDragDropComponent implements OnInit {

  @Input() formGroup: FormGroup;
  public syntaxError: boolean = false;

  ngOnInit() {
  }

  uploadFile(event) {
    const file = event[0];
    const fileReader = new FileReader();
    fileReader.readAsText(file, 'UTF-8');
    fileReader.onload = () => {
      if (typeof fileReader.result === 'string') {
        this.syntaxError = false;
        this.formGroup.get('format').setValue(event[0].type);
        this.formGroup.get('name').setValue(event[0].name);
        this.formGroup.get('size').setValue(event[0].size);
        try {
          this.formGroup.get('file').setValue(JSON.parse(fileReader.result));
        } catch (err) {
          console.log(err);
          this.syntaxError = true;
          this.formGroup.get('file').setValue(null);
        }
      }
    };
    fileReader.onerror = (error) => {
       console.log(error);
       this.syntaxError = true;
    };
  }
}
