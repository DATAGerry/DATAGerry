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

import { Component, OnDestroy, OnInit } from '@angular/core';
import { AuthSettingsService } from '../services/auth-settings.service';
import { forkJoin, Observable, Subscription } from 'rxjs';
import { FormArray, FormControl, FormGroup } from '@angular/forms';
import { CmdbMode } from '../../framework/modes.enum';
import { NgxSpinnerService } from 'ngx-spinner';
import { ToastService } from '../../layout/toast/toast.service';

@Component({
  selector: 'cmdb-auth-settings',
  templateUrl: './auth-settings.component.html',
  styleUrls: ['./auth-settings.component.scss']
})
export class AuthSettingsComponent implements OnInit, OnDestroy {

  // Params
  public renderMode = CmdbMode.Edit;
  public isPatched: boolean = false;

  // Form
  public authProviderFormGroup: FormGroup;
  public authSettingsFormConfig: any[] = [
    {
    name: 'enable_external',
    label: 'Enable External',
    type: 'checkbox'
    },
    {
      name: 'token_lifetime',
      label: 'Token lifetime',
      description: 'How long should the token be valid?',
      type: 'number'
    }
  ];
  public authProviderControlConfigFormMap: Map<string, any> = new Map<string, any>();

  // Data
  public authSettings: any = undefined;
  public installedProviderList: any[];

  // Subscriptions
  private authSettingsSubscription: Subscription;
  private authProvidersSubscription: Subscription;
  private configFormSubscriptions: Subscription;
  private configFormSaveSubscriptions: Subscription;

  public constructor(private authSettingsService: AuthSettingsService, private spinner: NgxSpinnerService, private toast: ToastService) {
    this.authProviderFormGroup = new FormGroup({
      _id: new FormControl('auth'),
      enable_external: new FormControl(false),
      providers: new FormArray([])
    });
    this.authSettingsSubscription = new Subscription();
    this.authProvidersSubscription = new Subscription();
    this.configFormSubscriptions = new Subscription();
    this.configFormSaveSubscriptions = new Subscription();
  }

  public ngOnInit(): void {
    this.authProvidersSubscription = this.authSettingsService.getProviders().subscribe((providers: any[]) => {
      this.installedProviderList = providers;
    });
    this.authSettingsSubscription = this.authSettingsService.getSettings().subscribe((settings: any) => {
      this.authSettings = settings;
      const providersFormArray = this.authProviderFormGroup.get('providers') as FormArray;
      const configFormRequests: Observable<any>[] = [];
      for (const provider of this.authSettings.providers) {
        configFormRequests.push(this.authSettingsService.getProviderConfigForm(provider.class_name));
      }
      this.configFormSubscriptions = forkJoin(configFormRequests).subscribe((configForms: any[]) => {
        // tslint:disable-next-line:prefer-for-of
        for (let i = 0; i < this.authSettings.providers.length; i++) {
          this.authProviderControlConfigFormMap.set(this.authSettings.providers[i].class_name, configForms[i]);
          const providerFormGroup = new FormGroup({
            class_name: new FormControl(this.authSettings.providers[i].class_name),
            config: new FormGroup({})
          });
          const configGroup = providerFormGroup.get('config') as FormGroup;

          this.addEntriesToFormGroup(configGroup, configForms[i].entries);
          this.addSectionToFormGroup(configGroup, configForms[i].sections);
          providersFormArray.push(providerFormGroup);
        }
        this.patchDatabaseValues();
      });

    });
  }

  private patchDatabaseValues(): void {
    this.authProviderFormGroup.patchValue(this.authSettings);
    this.isPatched = true;
  }

  private addEntriesToFormGroup(group: FormGroup, entries: any[] = []) {
    if (entries.length > 0) {
      for (const entry of entries) {
        group.addControl(entry.name, new FormControl(entry.default));
      }
    }
  }

  private addSectionToFormGroup(group: FormGroup, sections: any[] = []) {
    if (sections.length > 0) {
      for (const section of sections) {
        const sectionFormGroup = new FormGroup({});
        this.addEntriesToFormGroup(sectionFormGroup, section.entries);
        group.addControl(section.name, sectionFormGroup);
      }
    }
  }

  public getProviderConfigFormGroup(index: number): FormGroup {
    const providersList = this.authProviderFormGroup.get('providers') as FormArray;
    const providerFormGroup = providersList.at(index);
    return providerFormGroup.get('config') as FormGroup;
  }

  public getProviderConfigSectionFormGroup(index: number, sectionName: string): FormGroup {
    return this.getProviderConfigFormGroup(index).get(sectionName) as FormGroup;
  }

  public getInstalledProviderByName(providerName: string): any {
    return this.installedProviderList.find(provider => provider.class_name === providerName);
  }

  public onSave(): void {
    if (this.authProviderFormGroup.valid) {
      this.spinner.show();
      this.configFormSaveSubscriptions = this.authSettingsService.postSettings(this.authProviderFormGroup.value).subscribe((resp: any) => {
        this.toast.show('Authentication config was updated!');
      }).add(() => {
        this.spinner.hide();
      });
    }
  }

  public ngOnDestroy(): void {
    this.authSettingsSubscription.unsubscribe();
    this.authProvidersSubscription.unsubscribe();
    this.configFormSubscriptions.unsubscribe();
    this.configFormSaveSubscriptions.unsubscribe();
  }

}
