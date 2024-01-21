/*
* DATAGERRY - OpenSource Enterprise CMDB
* Copyright (C) 2024 becon GmbH
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
* along with this program. If not, see <https://www.gnu.org/licenses/>.
*/

import { Component, OnInit } from '@angular/core';
import { UntypedFormControl, UntypedFormGroup, Validators } from '@angular/forms';
import {
  DocapiBuilderTypeStepBaseComponent
} from '../docapi-builder-type-step/docapi-builder-type-step-base/docapi-builder-type-step-base.component';
import { CmdbType } from '../../../framework/models/cmdb-type';
import { TypeService } from '../../../framework/services/type.service';

@Component({
  selector: 'cmdb-docapi-settings-builder-type-step-objectlist',
  templateUrl: './docapi-builder-type-step-objectlist.component.html',
  styleUrls: ['./docapi-builder-type-step-objectlist.component.scss']
})
export class DocapiBuilderTypeStepObjectlistComponent
  extends DocapiBuilderTypeStepBaseComponent implements OnInit {

  public objectTypeList: Array<CmdbType> = [];

  constructor(private typeService: TypeService) {
    super();
    // setup form
    this.typeParamForm = new UntypedFormGroup({
      type: new UntypedFormControl('', Validators.required)
    });
  }

  ngOnInit() {
    // load object type list
    this.typeService.getTypeList().subscribe((value: CmdbType[]) => this.objectTypeList = value);
  }
}
