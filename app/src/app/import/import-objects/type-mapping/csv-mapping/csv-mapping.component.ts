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
import { TypeMappingBaseComponent } from '../type-mapping-base.component';
import { ImportService } from '../../../import.service';

@Component({
  selector: 'cmdb-csv-mapping',
  templateUrl: './csv-mapping.component.html',
  styleUrls: ['./csv-mapping.component.scss']
})
export class CsvMappingComponent extends TypeMappingBaseComponent implements OnInit, OnDestroy {

  constructor(public importerService: ImportService) {
    super(importerService);
  }

  public ngOnInit(): void {
    this.parsedDataSubscription = this.getParsedData(this.importerFile.file, this.parserConfig).subscribe(data => {
      console.log(data);
    });
  }

  public ngOnDestroy(): void {
    this.parsedDataSubscription.unsubscribe();
  }


}
