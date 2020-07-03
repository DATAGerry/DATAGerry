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

import { Component, OnInit, Input } from '@angular/core';
import { AbstractControl, FormControl, FormGroup, Validators } from '@angular/forms';
import { CmdbType } from '../../../../../framework/models/cmdb-type';
import { TypeService } from '../../../../../framework/services/type.service';
import { DocapiSettingsBuilderTypeStepBaseComponent } from '../docapi-settings-builder-type-step-base/docapi-settings-builder-type-step-base.component';

@Component({
  selector: 'cmdb-docapi-settings-builder-type-step-object',
  templateUrl: './docapi-settings-builder-type-step-object.component.html',
  styleUrls: ['./docapi-settings-builder-type-step-object.component.scss']
})
export class DocapiSettingsBuilderTypeStepObjectComponent extends DocapiSettingsBuilderTypeStepBaseComponent implements OnInit {


  public objectTypeList: CmdbType[] = [];

  constructor(private typeService: TypeService) { 
    super();
    //setup form
    this.typeParamForm = new FormGroup({
      type: new FormControl('', Validators.required)
    });
  }

  ngOnInit() {
    //load object type list
    this.typeService.getTypeList().subscribe((value: CmdbType[]) => this.objectTypeList = value);
  }

}
