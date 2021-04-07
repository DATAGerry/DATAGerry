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

import { Component, OnInit, Input } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { DocapiService, checkDocTemplateExistsValidator } from '../../docapi.service';
import { CmdbMode } from '../../../framework/modes.enum';

@Component({
  selector: 'cmdb-docapi-settings-builder-settings-step',
  templateUrl: './docapi-builder-settings-step.component.html',
  styleUrls: ['./docapi-builder-settings-step.component.scss']
})
export class DocapiBuilderSettingsStepComponent implements OnInit {

  @Input()
  set preData(data: any) {
    if (data !== undefined) {
      this.settingsForm.patchValue(data);
    }
  }

  @Input() public mode: CmdbMode;
  public modes = CmdbMode;
  public settingsForm: FormGroup;

  constructor(private docapiService: DocapiService) {
    this.settingsForm = new FormGroup({
      name: new FormControl('', Validators.required),
      label: new FormControl('', Validators.required),
      description: new FormControl(''),
      active: new FormControl(true)
    });
  }

  public get name() {
    return this.settingsForm.get('name');
  }

  public get label() {
    return this.settingsForm.get('label');
  }


  ngOnInit() {
    if (this.mode === CmdbMode.Create) {
      this.settingsForm.get('name').setAsyncValidators(checkDocTemplateExistsValidator(this.docapiService));
      this.settingsForm.get('label').valueChanges.subscribe(value => {
        this.settingsForm.get('name').setValue(value.replace(/ /g, '-').toLowerCase());
        const newValue = this.settingsForm.get('name').value;
        this.settingsForm.get('name').setValue(newValue.replace(/[^a-z0-9 \-]/gi, '').toLowerCase());
        this.settingsForm.get('name').markAsDirty({ onlySelf: true });
        this.settingsForm.get('name').markAsTouched({ onlySelf: true });
      });
    } else if (CmdbMode.Edit) {
      this.settingsForm.markAllAsTouched();
    }
  }

}
