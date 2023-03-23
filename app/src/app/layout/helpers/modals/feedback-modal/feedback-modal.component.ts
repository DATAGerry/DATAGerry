/*
* DATAGERRY - OpenSource Enterprise CMDB
* Copyright (C) 2023 becon GmbH
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

import { Component, OnDestroy, OnInit } from '@angular/core';
import { SystemService } from '../../../../settings/system/system.service';
import { UntypedFormControl, UntypedFormGroup, Validators } from '@angular/forms';
import { Subscription } from 'rxjs';
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';

@Component({
  selector: 'cmdb-feedback-modal',
  templateUrl: './feedback-modal.component.html',
  styleUrls: ['./feedback-modal.component.scss']
})
export class FeedbackModalComponent implements OnInit, OnDestroy {

  public feedbackForm: UntypedFormGroup;
  public formListener: Subscription;
  public feedbackUrl: string = 'https://datagerry.com/feedback-v1/0/0/0/0/0/unknown/';

  constructor(private systemService: SystemService, public activeModal: NgbActiveModal) {
    this.feedbackForm = new UntypedFormGroup({
      happiness: new UntypedFormControl(0),
      usability: new UntypedFormControl(0),
      functionality: new UntypedFormControl(0),
      performance: new UntypedFormControl(0),
      stability: new UntypedFormControl(0),
      version: new UntypedFormControl(''),
      email: new UntypedFormControl('', [
        Validators.email, Validators.pattern('^[a-z0-9._%+-]+@[a-z0-9.-]+\\.[a-z]{2,4}$')
      ]),
    });
  }

  public get emailController(): UntypedFormControl {
    return this.feedbackForm.get('email') as UntypedFormControl;
  }

  public ngOnInit(): void {
    this.systemService.getDatagerryInformation().subscribe((infos: any) => {
      this.feedbackForm.get('version').setValue(infos.version);
    });

    this.formListener = this.feedbackForm.valueChanges.subscribe(value => {
      this.generateQRCode();
    });
  }

  private generateQRCode(): void {
    let url = 'https://datagerry.com/feedback-v1/';
    url = url + this.feedbackForm.get('happiness').value.toString() + '/'
      + this.feedbackForm.get('usability').value.toString() + '/'
      + this.feedbackForm.get('functionality').value.toString() + '/'
      + this.feedbackForm.get('performance').value.toString() + '/'
      + this.feedbackForm.get('stability').value.toString() + '/'
      + this.feedbackForm.get('version').value.toString() + '/'
      + this.feedbackForm.get('email').value.toString();
    this.feedbackUrl = url;
  }

  public ngOnDestroy(): void {
    this.formListener.unsubscribe();
  }
}
