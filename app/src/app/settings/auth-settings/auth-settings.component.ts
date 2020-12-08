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
import { ReplaySubject } from 'rxjs';
import { FormArray, FormControl, FormGroup } from '@angular/forms';
import { ToastService } from '../../layout/toast/toast.service';
import { ProgressSpinnerService } from '../../layout/progress/progress-spinner.service';
import { takeUntil } from 'rxjs/operators';
import { AuthService } from '../../auth/services/auth.service';
import { ActivatedRoute, Data } from '@angular/router';
import { AuthProvider } from '../../auth/models/providers';
import { AuthSettings } from '../../auth/models/settings';

@Component({
  selector: 'cmdb-auth-settings',
  templateUrl: './auth-settings.component.html',
  styleUrls: ['./auth-settings.component.scss']
})
export class AuthSettingsComponent implements OnInit, OnDestroy {

  /**
   * Un-subscriber for `AuthSettingsComponent`.
   * @private
   */
  private subscriber: ReplaySubject<void> = new ReplaySubject<void>();

  public authConfigForm: FormGroup;
  public authSettings: AuthSettings;

  public installedProviderList: Array<AuthProvider>;

  public constructor(private authSettingsService: AuthService, private activateRoute: ActivatedRoute,
                     private spinner: ProgressSpinnerService, private toast: ToastService) {
    this.authConfigForm = new FormGroup({
      _id: new FormControl('auth'),
      enable_external: new FormControl(false),
      token_lifetime: new FormControl(null),
      providers: new FormArray([])
    });
    this.activateRoute.data.pipe(takeUntil(this.subscriber)).subscribe((data: Data) => {
      this.installedProviderList = data.providers;
    });
  }

  public ngOnInit(): void {
    this.authSettingsService.getSettings().pipe(takeUntil(this.subscriber)).subscribe((settings: any) => {
      this.authSettings = settings;
      this.authConfigForm.patchValue(this.authSettings);
    });
  }

  public get providersArray(): FormArray {
    return this.authConfigForm.get('providers') as FormArray;
  }

  public onSave(): void {
    if (this.authConfigForm.valid) {
      this.authSettingsService.postSettings(this.authConfigForm.getRawValue()).pipe(takeUntil(this.subscriber)).subscribe(() => {
        this.toast.success('Authentication config was updated!');
      });
    }
  }

  public ngOnDestroy(): void {
    this.subscriber.next();
    this.subscriber.complete();
  }

}
