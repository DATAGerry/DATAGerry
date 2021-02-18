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
* along with this program. If not, see <https://www.gnu.org/licenses/>.
*/

import { Component, OnInit, Input, ViewChild, EventEmitter, Output } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { CmdbMode } from '../../../../framework/modes.enum';
import {
  DocapiSettingsBuilderTypeStepBaseComponent
} from './docapi-settings-builder-type-step-base/docapi-settings-builder-type-step-base.component';

@Component({
  selector: 'cmdb-docapi-settings-builder-type-step',
  templateUrl: './docapi-settings-builder-type-step.component.html',
  styleUrls: ['./docapi-settings-builder-type-step.component.scss']
})
export class DocapiSettingsBuilderTypeStepComponent implements OnInit {

  @Input()
  set preData(data: any) {
    if (data !== undefined) {
      this.typeForm.patchValue(data);
      if (data.template_parameters) {
        this.typeParamPreData = data.template_parameters;
      }
    }
  }

  @Input() public mode: CmdbMode;
  public modes = CmdbMode;
  public typeForm: FormGroup;
  public readonly docTypeSelect: any[] = [
    { label: 'Object Template', content: 'OBJECT', description: 'Template for single objects' }
  ];

  @ViewChild('typeparam')
  public typeParamComponent: DocapiSettingsBuilderTypeStepBaseComponent;
  public typeParamPreData: any;

  public typeValid: boolean = false;
  public typeChildValid: boolean = false;

  @Output() public formValidEmitter: EventEmitter<boolean>;


  constructor() {
    // setup form
    this.formValidEmitter = new EventEmitter<boolean>();
    this.typeForm = new FormGroup({
      template_type: new FormControl('', Validators.required)
    });
  }

  public ngOnInit(): void {
    this.typeForm.valueChanges.subscribe(() => {
      this.typeValid = this.typeForm.valid;
      this.formValidEmitter.emit(this.typeValid && this.typeChildValid);
    });
  }

}
