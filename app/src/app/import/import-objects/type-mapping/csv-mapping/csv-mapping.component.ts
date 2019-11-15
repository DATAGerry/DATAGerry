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
import { FormControl, FormGroup } from '@angular/forms';
import { Subscription } from 'rxjs';

@Component({
  selector: 'cmdb-csv-mapping',
  templateUrl: './csv-mapping.component.html',
  styleUrls: ['./csv-mapping.component.scss']
})
export class CsvMappingComponent extends TypeMappingBaseComponent implements OnInit, OnDestroy {

  public previewIndex: number = 0;
  public previewIndexSelectionForm: FormGroup;
  private previewSelectionSubscription: Subscription;

  constructor() {
    super();
    this.previewIndexSelectionForm = new FormGroup({
      indexSelection: new FormControl(0)
    });
    this.previewSelectionSubscription = this.previewIndexSelectionForm.get('indexSelection').valueChanges
      .subscribe((change) => {
        this.previewIndex = +change;
      });
  }


  public ngOnInit(): void {
    for (let i = 0; i < this.parsedData.entry_length; i++) {
      this.currentMapping.push({});
    }
  }

  public ngOnDestroy(): void {
    this.previewSelectionSubscription.unsubscribe();
  }

  public onAutoSet(): void{

  }

}
