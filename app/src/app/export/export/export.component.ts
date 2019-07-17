/*
* dataGerry - OpenSource Enterprise CMDB
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
import { HttpHeaders } from '@angular/common/http';
import { ExportService } from '../../services/export.service';
import { DatePipe } from '@angular/common';
import { CmdbType } from '../../framework/models/cmdb-type';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { TypeService } from '../../framework/services/type.service';

@Component({
  selector: 'cmdb-export',
  templateUrl: './export.component.html',
  styleUrls: ['./export.component.scss']
})
export class ExportComponent implements OnInit {

  public typeList: CmdbType[];
  public formExport: FormGroup;
  public isSubmitted = false;
  readonly URL: string = '/object/type/';

  constructor(private exportService: ExportService, private datePipe: DatePipe, private typeService: TypeService) {
    this.formExport = new FormGroup({
      type: new FormControl(null, Validators.required),
      format: new FormControl('', Validators.required)
    });
  }

  ngOnInit() {
    this.typeService.getTypeList().subscribe((list: CmdbType[]) => {
      this.typeList = list;
    });
  }

  get type() {
    return this.formExport.get('type');
  }

  get format() {
    return this.formExport.get('format');
  }

  changeType(e) {
    this.type.setValue(e.target.value, {
      onlySelf: true
    });
  }

  changeFormat(e) {
    this.format.setValue(e.target.value, {
      onlySelf: true
    });
  }

  public exportObjectByTypeID() {

    console.log(this.type);

    this.isSubmitted = true;
    if (!this.formExport.valid) {
      return false;
    }

    const typeID: any = this.formExport.get('type').value;
    let fileExtension: string = this.formExport.get('format').value;

    console.log(typeID);

    if (fileExtension != null && typeID != null) {
      fileExtension = fileExtension.toLocaleLowerCase();

      const httpHeader = new HttpHeaders({
        'Content-Type': 'application/' + fileExtension
      });
      this.exportService.callExportRoute('export/' + fileExtension + this.URL + typeID, fileExtension, httpHeader);
    }
  }
}
