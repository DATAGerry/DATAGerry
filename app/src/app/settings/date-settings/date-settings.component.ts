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
import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'cmdb-date-settings',
  templateUrl: './date-settings.component.html',
  styleUrls: ['./date-settings.component.scss']
})
export class DateSettingsComponent implements OnInit {

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

  ngOnInit(): void {
    this.regionalForm = new FormGroup({
      format: new FormControl('YYYY-MM-DD', Validators.required),
      timezone: new FormControl(moment.tz.guess(true)),
    });
    this.regionalForm.valueChanges.subscribe(() => {
      console.log('test');
      this.updateFormatView();
    });
    this.updateFormatView();
  }

  /**
   * return current format value from formGroup
   */
  public get format(): string {
    return this.regionalForm.get('format').value;
  }

  /**
   * return current timezone value from formGroup
   */
  public get timezone(): string {
    return this.regionalForm.get('timezone').value;
  }

  public updateFormatView(): void {
    this.displayTzF = moment.tz(moment(), this.timezone).format(this.format);
  }

  public utcToDeviceString(timezone: string): string {
    const utc = moment.tz(moment(), timezone).format('( UTC Z )');
    return timezone + ' ' + utc;
  }
}
