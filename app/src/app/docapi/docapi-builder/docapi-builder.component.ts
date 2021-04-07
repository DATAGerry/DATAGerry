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

import { Component, Input, ViewChild } from '@angular/core';
import { Router } from '@angular/router';
import { ToastService } from '../../layout/toast/toast.service';
import { CmdbMode } from '../../framework/modes.enum';
import { DocapiService } from '../docapi.service';
import {
  DocapiBuilderSettingsStepComponent
} from './docapi-builder-settings-step/docapi-builder-settings-step.component';
import { DocapiBuilderTypeStepComponent } from './docapi-builder-type-step/docapi-builder-type-step.component';
import { DocapiBuilderStyleStepComponent } from './docapi-builder-style-step/docapi-builder-style-step.component';
import {
  DocapiBuilderContentStepComponent
} from './docapi-builder-content-step/docapi-builder-content-step.component';
import { DocTemplate } from '../models/cmdb-doctemplate';

@Component({
  selector: 'cmdb-docapi-settings-builder',
  templateUrl: './docapi-builder.component.html',
  styleUrls: ['./docapi-builder.component.scss']
})
export class DocapiBuilderComponent {

  @Input() public mode: number = CmdbMode.Create;
  @Input() public docInstance?: DocTemplate;

  @ViewChild(DocapiBuilderSettingsStepComponent, { static: true })
  public settingsStep: DocapiBuilderSettingsStepComponent;

  @ViewChild(DocapiBuilderTypeStepComponent, { static: true })
  public typeStep: DocapiBuilderTypeStepComponent;
  public typeStepFormValid: boolean = false;
  public typeParam: any = undefined;

  @ViewChild(DocapiBuilderContentStepComponent, { static: true })
  public contentStep: DocapiBuilderContentStepComponent;

  @ViewChild(DocapiBuilderStyleStepComponent, { static: true })
  public styleStep: DocapiBuilderStyleStepComponent;

  constructor(private docapiService: DocapiService, private router: Router, private toast: ToastService) {
  }

  public saveDoc() {
    if (this.mode === CmdbMode.Create) {
      this.docInstance = new DocTemplate();
    }
    this.docInstance.name = this.settingsStep.settingsForm.get('name').value;
    this.docInstance.label = this.settingsStep.settingsForm.get('label').value;
    this.docInstance.active = this.settingsStep.settingsForm.get('active').value;
    this.docInstance.description = this.settingsStep.settingsForm.get('description').value;
    this.docInstance.template_type = this.typeStep.typeForm.get('template_type').value;
    this.docInstance.template_parameters = this.typeStep.typeParamComponent.typeParamForm.value;
    this.docInstance.template_data = this.contentStep.contentForm.get('template_data').value;
    this.docInstance.template_style = this.styleStep.styleForm.get('template_style').value;

    if (this.mode === CmdbMode.Create) {
      let newId = null;
      this.docapiService.postDocTemplate(this.docInstance).subscribe(publicIdResp => {
          newId = publicIdResp;
          this.router.navigate(['settings/docapi/'], { queryParams: { docAddSuccess: newId } });
        },
        (error) => {
          console.error(error);
        });
    } else if (this.mode === CmdbMode.Edit) {
      this.docapiService.putDocTemplate(this.docInstance).subscribe((updateResp: DocTemplate) => {
          this.toast.success(`DocAPI document successfully edited: ${ updateResp.public_id }`);
          this.router.navigate(['/settings/docapi/'], { queryParams: { docEditSuccess: updateResp.public_id } });
        },
        (error) => {
          console.error(error);
        });
    }

  }

}
