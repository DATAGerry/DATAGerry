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
* along with this program.  If not, see <https://www.gnu.org/licenses/>.
*/

import { Component, OnDestroy, OnInit } from '@angular/core';
import { DebugService } from './debug.service';
import { BackendHttpError } from '../error/models/custom.error';
import { UntypedFormControl, UntypedFormGroup, Validators } from '@angular/forms';
import { Subscription } from 'rxjs';

@Component({
  selector: 'cmdb-debug',
  templateUrl: './debug.component.html',
  styleUrls: ['./debug.component.scss']
})
export class DebugComponent implements OnInit, OnDestroy {

  private httpResponseSubscription: Subscription;
  private customHttpResponseSubscription: Subscription;

  public customResponse: BackendHttpError = null;
  public customResponseForm: UntypedFormGroup;

  public constructor(private debugService: DebugService) {
    this.httpResponseSubscription = new Subscription();
    this.customHttpResponseSubscription = new Subscription();
  }

  public ngOnInit(): void {
    this.customResponseForm = new UntypedFormGroup({
      customStatus: new UntypedFormControl(400, Validators.required),
      customMessage: new UntypedFormControl('')
    });
  }

  public onStartHttpResponse(statusCode: number) {
    this.debugService.getResponse(statusCode).subscribe(resp => {
        // this should not happen
      },
      (error) => {
        document.getElementById(`http_${ statusCode }_response`).innerHTML = error.error.description;
      });
  }

  public onCustomResponse() {
    if (this.customResponseForm.valid) {
      this.debugService.getResponseWithMessage(
        this.customResponseForm.get('customStatus').value,
        this.customResponseForm.get('customMessage').value,
        ).subscribe(() => {
        // this should not happen
      }, (error) => {
          this.customResponse = error.error as BackendHttpError;
      });
    }

  }

  public ngOnDestroy(): void {
    this.httpResponseSubscription.unsubscribe();
    this.customHttpResponseSubscription.unsubscribe();
  }
}
