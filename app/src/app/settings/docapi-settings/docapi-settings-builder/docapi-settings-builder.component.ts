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

import { Component, OnInit, Input, ViewChild } from '@angular/core';
import { Router } from '@angular/router';
import { ToastService } from '../../../layout/toast/toast.service';
import { CmdbMode } from '../../../framework/modes.enum';
import { DocTemplate } from '../../../framework/models/cmdb-doctemplate';
import { DocapiService } from '../../../docapi/docapi.service';
import { DocapiSettingsBuilderSettingsStepComponent } from './docapi-settings-builder-settings-step/docapi-settings-builder-settings-step.component';
import { DocapiSettingsBuilderTypeStepComponent } from './docapi-settings-builder-type-step/docapi-settings-builder-type-step.component';
import { DocapiSettingsBuilderStyleStepComponent } from './docapi-settings-builder-style-step/docapi-settings-builder-style-step.component';
import { DocapiSettingsBuilderContentStepComponent } from './docapi-settings-builder-content-step/docapi-settings-builder-content-step.component';

@Component({
  selector: 'cmdb-docapi-settings-builder',
  templateUrl: './docapi-settings-builder.component.html',
  styleUrls: ['./docapi-settings-builder.component.scss']
})
export class DocapiSettingsBuilderComponent implements OnInit {

  @Input() public mode: number = CmdbMode.Create;
  @Input() public docInstance?: DocTemplate;

  @ViewChild(DocapiSettingsBuilderSettingsStepComponent, { static: true })
  public settingsStep: DocapiSettingsBuilderSettingsStepComponent;

  @ViewChild(DocapiSettingsBuilderTypeStepComponent, { static: true })
  public typeStep: DocapiSettingsBuilderTypeStepComponent;
  public typeStepFormValid: boolean = false;
  public typeParam: any = undefined;

  @ViewChild(DocapiSettingsBuilderContentStepComponent, { static: true })
  public contentStep: DocapiSettingsBuilderContentStepComponent;

  @ViewChild(DocapiSettingsBuilderStyleStepComponent, { static: true })
  public styleStep: DocapiSettingsBuilderStyleStepComponent;

  constructor(private docapiService: DocapiService, private router: Router, private toast: ToastService) {
  }

  ngOnInit() {
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
          this.toast.show(`DocAPI document successfully edited: ${ updateResp.public_id }`);
          this.router.navigate(['/settings/docapi/'], { queryParams: { docEditSuccess: updateResp.public_id } });
        },
        (error) => {
          console.error(error);
        });
    }

  }

}
