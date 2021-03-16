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

import * as moment from 'moment';
import 'moment-timezone';
import { Component, OnDestroy, OnInit } from '@angular/core';
import { AbstractControl, FormControl, FormGroup, Validators } from '@angular/forms';
import { DateSettingsService } from '../services/date-settings.service';
import { takeUntil } from 'rxjs/operators';
import { ReplaySubject } from 'rxjs';
import { ToastService } from '../../layout/toast/toast.service';

@Component({
  selector: 'cmdb-date-settings',
  templateUrl: './date-settings.component.html',
  styleUrls: ['./date-settings.component.scss']
})
export class DateSettingsComponent implements OnInit, OnDestroy {

  /**
   * Un-subscriber for `DateSettingsComponent`.
   * @private
   */
  private subscriber: ReplaySubject<void> = new ReplaySubject<void>();

  /**
   * All time zones of MomentTimezone
   */
  public tzNames: string[] = moment.tz.names();

  /**
   * Example view for date format with selected settings
   */
  public displayTzF: string;

  /**
   * ISO 8601 date formats
   */
  public formats: any[] = [
    {id: 'short', format: 'YYYY-MM-DD', view:  '2013-07-16'},
    {id: 'medium', format: 'YYYY-MM-DDThh', view: '2013-07-16T19'},
    {id: 'mediumZ', format: 'YYYY-MM-DDThhZ', view: '2013-07-16T19Z'},
    {id: 'long', format: 'YYYY-MM-DDThh:mm', view: '2013-07-16T19:23'},
    {id: 'longZ', format: 'YYYY-MM-DDThh:mmZ', view: '2013-07-16T19:23Z'},
    {id: 'full', format: 'YYYY-MM-DDThh:mm:ss', view: '2013-07-16T19:23:51Z'},
    {id: 'fullZ', format: 'YYYY-MM-DDThh:mm:ssZ', view: '2013-07-16T19:23:51Z'}
  ];

  /**
   * FromGroup Regional Settings
   */
  public regionalForm: FormGroup;

  constructor(private dateSettingsService: DateSettingsService, private toast: ToastService) {
    this.regionalForm = new FormGroup({
      date_format: new FormControl('YYYY-MM-DD', Validators.required),
      timezone: new FormControl(moment.tz.guess(true)),
    });
  }

  ngOnInit(): void {
    this.dateSettingsService.getDateSettings().pipe(takeUntil(this.subscriber)).subscribe((dateSettings: any) => {
      this.regionalForm.patchValue(dateSettings);
    });

    this.regionalForm.valueChanges.subscribe(() => {
      this.updateFormatView();
    });
    this.updateFormatView();
  }

  /**
   * return controller from formGroup by name
   */
  public getController(name: string): AbstractControl {
    return this.regionalForm.get(name);
  }

  /**
   * return current format value from formGroup
   */
  public get format(): string {
    return this.regionalForm.get('date_format').value;
  }

  /**
   * return current timezone value from formGroup
   */
  public get timezone(): string {
    return this.regionalForm.get('timezone').value;
  }

  /**
   * Update example view for date format with selected settings
   */
  public updateFormatView(): void {
    this.displayTzF = moment.tz(moment(), this.timezone).format(this.format);
  }

  /**
   * Display Time Difference to Time Zone – UTC
   * @param timezone
   */
  public utcToDeviceString(timezone: string): string {
    const utc = moment.tz(moment(), timezone).format('( UTC Z )');
    return timezone + ' ' + utc;
  }

  public onSave(): void {
    if (this.regionalForm.valid) {
      this.dateSettingsService.postDateSettings(this.regionalForm.getRawValue())
        .pipe(takeUntil(this.subscriber)).subscribe(() => {
          this.toast.success('Date Settings config was updated!');
      });
    }
  }

  public ngOnDestroy(): void {
    this.subscriber.next();
    this.subscriber.complete();
  }
}
