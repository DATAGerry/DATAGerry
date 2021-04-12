/*
* DATAGERRY - OpenSource Enterprise CMDB
* Copyright (C) 2019 - 2021 NETHINKS GmbH
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

import { Component, Input } from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';
import { CmdbMode } from '../../../framework/modes.enum';

@Component({
  selector: 'cmdb-docapi-settings-builder-style-step',
  templateUrl: './docapi-builder-style-step.component.html',
  styleUrls: ['./docapi-builder-style-step.component.scss']
})
export class DocapiBuilderStyleStepComponent {

  @Input()
  set preData(data: any) {
    if (data !== undefined) {
      this.styleForm.patchValue(data);
    }
  }

  @Input() public mode: CmdbMode;
  public modes = CmdbMode;
  public styleForm: FormGroup;

  constructor() {
    this.styleForm = new FormGroup({
      template_style: new FormControl('')
    });
  }


}
