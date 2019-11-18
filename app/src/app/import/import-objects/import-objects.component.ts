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
import { ImporterConfig, ImporterFile, ImportResponse } from './import-object.models';
import { ImportService } from '../import.service';
import { Subscription } from 'rxjs';
import { NgxSpinner } from 'ngx-spinner/lib/ngx-spinner.enum';
import { NgxSpinnerService } from 'ngx-spinner';

@Component({
  selector: 'cmdb-import-objects',
  templateUrl: './import-objects.component.html',
  styleUrls: ['./import-objects.component.scss']
})
export class ImportObjectsComponent implements OnInit, OnDestroy {

  private fileReader: FileReader;
  public typeInstance: CmdbType = undefined;

  // Importer Data
  private importerSubscription: Subscription;
  public importerFile: ImporterFile = {} as ImporterFile;
  public importerConfig: ImporterConfig = {} as ImporterConfig;
  // at the moment only MAPPING
  public defaultImporterConfig: any;

  // Parser Data
  private parseDataSubscription: Subscription;
  public parserConfig: any = {};
  public parsedData: any = undefined;

  // Import Response
  public importResponse: ImportResponse = undefined;

  public constructor(private importService: ImportService, private spinner: NgxSpinnerService) {
    this.fileReader = new FileReader();
    this.importerSubscription = new Subscription();
    this.parseDataSubscription = new Subscription();
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
    this.importerSubscription.unsubscribe();
    this.parseDataSubscription.unsubscribe();
  }

  public formatChange(format: string) {
    this.importerFile.fileFormat = format;
    const defaultImporterConfig = this.importService.getObjectImporterDefaultConfig(this.importerFile.fileFormat)
      .subscribe((defaultConfig: any) => {
          this.defaultImporterConfig = defaultConfig;
        },
        (error) => console.error(error),
        () => defaultImporterConfig.unsubscribe()
      );
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
    this.importerConfig.type_id = this.typeInstance.public_id as number;
  }

  public typeChange(change: any) {
    this.importerConfig.type_id = change.typeID as number;
    this.typeInstance = change.typeInstance as CmdbType;
  }

  public onParseData() {
    this.spinner.show();
    this.parseDataSubscription = this.importService.postObjectParser(this.importerFile.file, this.parserConfig).subscribe(
      (parsedData) => {
        this.parsedData = parsedData;
      },
      (e) => console.error(e),
      () => {
        this.spinner.hide();
      }
    );
  }

  public startImport() {
    this.spinner.show();
    this.importService.importObjects(this.importerFile.file, this.parserConfig, this.importerConfig).subscribe(
      (importResponse) => {
        this.importResponse = importResponse;
      },
      (error) => {
        console.error(error);
        this.spinner.hide();
      },
      () => {
        this.spinner.hide();
      }
    );
  }

}
