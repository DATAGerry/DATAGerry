/*
* DATAGERRY - OpenSource Enterprise CMDB
* Copyright (C) 2019 - 2020 NETHINKS GmbH
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
import { SystemService } from '../../../settings/system/system.service';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { Subscription } from 'rxjs';

@Component({
  selector: 'cmdb-feedback-form',
  templateUrl: './feedback-form.component.html',
  styleUrls: ['./feedback-form.component.scss']
})
export class FeedbackFormComponent implements OnInit, OnDestroy {

  public feedbackForm: FormGroup;
  public formListener: Subscription;
  public feedbackUrl: string = 'https://datagerry.com/feedback-v1/0/0/0/0/0/unknown/';

  constructor(private systemService: SystemService) {
    this.feedbackForm = new FormGroup({
      happiness: new FormControl(0),
      usability: new FormControl(0),
      functionality: new FormControl(0),
      performance: new FormControl(0),
      stability: new FormControl(0),
      version: new FormControl(''),
      email: new FormControl('', [
        Validators.email, Validators.pattern('^[a-z0-9._%+-]+@[a-z0-9.-]+\\.[a-z]{2,4}$')
      ]),
    });
  }

  public get emailController(): FormControl {
    return this.feedbackForm.get('email') as FormControl;
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
