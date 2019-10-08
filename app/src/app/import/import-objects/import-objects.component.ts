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

import { Component, OnDestroy, OnInit } from '@angular/core';
import { CmdbType } from '../../framework/models/cmdb-type';
import { ImporterConfig, ImporterFile } from './import-object.models';

@Component({
  selector: 'cmdb-import-objects',
  templateUrl: './import-objects.component.html',
  styleUrls: ['./import-objects.component.scss']
})
export class ImportObjectsComponent implements OnInit, OnDestroy {

  private fileReader: FileReader;
  public typeInstance: CmdbType = undefined;
  public importerFile: ImporterFile = {} as ImporterFile;
  public parserConfig: any = {};
  public importerConfig: ImporterConfig = {} as ImporterConfig;


  public constructor() {
    this.fileReader = new FileReader();
  }

  public ngOnInit(): void {
    this.fileReader.onload = (e) => {
      this.importerFile.fileContent = this.fileReader.result;
    };
  }

  public ngOnDestroy(): void {
    if (this.fileReader.readyState !== FileReader.DONE) {
      this.fileReader.abort();
    }
  }

  public formatChange(format: string) {
    this.importerFile.fileFormat = format;
  }

  public fileChange(file: File) {
    this.importerFile.file = file;
    this.importerFile.fileName = file.name;
    this.fileReader.readAsText(file);
  }

  public parserConfigChange(config: any) {
    this.parserConfig = config;
  }

  public importConfigChange(config: any) {
    this.importerConfig = config as ImporterConfig;
  }

  public typeChange(change: any) {
    this.importerConfig.type_id = change.typeID as number;
    this.typeInstance = change.typeInstance as CmdbType;
  }

}
