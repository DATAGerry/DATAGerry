/*
* DATAGERRY - OpenSource Enterprise CMDB
* Copyright (C) 2024 becon GmbH
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

import { Component, Input, OnInit } from '@angular/core';
import { RenderFieldComponent } from '../components.fields';
import { formatDate } from '@angular/common';
import { NgbDateAdapter, NgbDateParserFormatter } from '@ng-bootstrap/ng-bootstrap';
import { NgbStringAdapter, CustomDateParserFormatter } from '../../../../settings/date-settings/date-settings-formatter.service';
import { takeUntil } from 'rxjs/operators';
import { DateSettingsService } from '../../../../settings/services/date-settings.service';
import { ReplaySubject } from 'rxjs';
import { FormGroup, FormControl } from '@angular/forms'; // Import FormGroup and FormControl


@Component({
  selector: 'cmdb-date',
  templateUrl: './date.component.html',
  styleUrls: ['./date.component.scss'],
  providers: [
    { provide: NgbDateAdapter, useClass: NgbStringAdapter },
    // { provide: NgbDateParserFormatter, useClass: CustomDateParserFormatter }
  ]
})
export class DateComponent extends RenderFieldComponent implements OnInit {

  /**
   * Un-subscriber for `DateSettingsComponent`.
   * @private
   */
  private subscriber: ReplaySubject<void> = new ReplaySubject<void>();
  public datePlaceholder = 'YYYY-MM-DD';

  public constructor(private dateSettingsService: DateSettingsService) {
    super();
  }

  ngOnInit(): void {
    if (this.parentFormGroup.get(this.data.name).value === '') {
      this.parentFormGroup.get(this.data.name).setValue(null, { onlySelf: true });
    }
    this.dateSettingsService.getDateSettings().pipe(takeUntil(this.subscriber)).subscribe((dateSettings: any) => {
      this.datePlaceholder = dateSettings.date_format;
    });
  }

  public get currentDate() {
    const currentDate = this.parentFormGroup.get(this.data.name).value;
    if (currentDate && currentDate.$date) {
      return new Date(currentDate.$date);
    }
    return currentDate;
  }

  public resetDate() {
    this.controller.setValue(null, { onlySelf: true });
    this.controller.reset();
    this.controller.markAsTouched();
    this.controller.markAsDirty();
  }

  public copyToClipboard() {
    const selBox = document.createElement('textarea');
    selBox.value = formatDate(this.currentDate, 'dd/MM/yyyy', 'en-US');
    this.generateDataForClipboard(selBox);
  }

  /**
   * Toggles the input type between 'date' and 'text' on double click.
   */

  onDblClick(event: MouseEvent) {
    const inputElement = event.target as HTMLInputElement;
    if (inputElement.type === 'date') {
      inputElement.type = 'text';

      setTimeout(() => {
        inputElement.select();
      });
    }
  }

  /**
   * Changes the input type back to 'date' when the input element loses focus,
   * if the current type is 'text'.
   */
  onFocusOut(event: FocusEvent) {
    const inputElement = event.target as HTMLInputElement;
    if (inputElement.type === 'text') {
      inputElement.type = 'date';
    }
  }

}
