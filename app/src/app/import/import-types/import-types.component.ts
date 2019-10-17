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
import { ImportService } from '../import.service';

@Component({
  selector: 'cmdb-import-types',
  templateUrl: './import-types.component.html',
  styleUrls: ['./import-types.component.scss']
})
export class ImportTypesComponent implements OnInit {

  public constructor(private importService: ImportService) {}

  public fileForm: FormGroup;
  public preview: any;
  public done: boolean = false;

  ngOnInit() {
    this.fileForm = new FormGroup({
      format: new FormControl('json', Validators.required),
      name: new FormControl('', Validators.required),
      size: new FormControl('', Validators.required),
      file: new FormControl(null, Validators.required),
    });

    this.fileForm.valueChanges.subscribe(newValue => {
      this.fileForm.get('file').patchValue(newValue.file, { onlySelf: true });
    });
  }

  public importTypeFile() {
    const theJSON = JSON.stringify(this.fileForm.get('file').value);
    const formData = new FormData();
    formData.append('uploadFile', theJSON);
    this.importService.postTypeParser(formData).subscribe(res => {
      console.log(res);
      this.done = true;
    });
  }

}
