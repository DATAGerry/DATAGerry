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
import { RenderField } from '../../fields/components.fields';
import { ReplaySubject } from 'rxjs';
import { takeUntil } from 'rxjs/operators';

@Component({
  selector: 'cmdb-object-bulk-input-appends',
  templateUrl: './object-bulk-input-appends.component.html',
  styleUrls: ['./object-bulk-input-appends.component.scss']
})
export class ObjectBulkInputAppendsComponent extends RenderField implements OnInit, OnDestroy {

  private unsubscribe: ReplaySubject<void> = new ReplaySubject<void>();
  public bulkControlName: string;

  constructor() {
    super();
  }


  ngOnInit() {
    this.bulkControlName = this.data.name + '-isChanged';
    this.controller.statusChanges.pipe(takeUntil(this.unsubscribe)).subscribe(() => {
      this.parentFormGroup.get(this.bulkControlName).setValue(true);
      this.changeCheckBox();
    });
  }

  public changeCheckBox(event: any = {checked: true}) {
    const {value} = this.parentFormGroup.get('changedFields');
    if (!event.checked) {
      value.delete(this.data.name);
    } else {
      value.set(this.data.name, this.data);
    }
  }

  ngOnDestroy(): void {
    this.unsubscribe.next();
    this.unsubscribe.complete();
  }
}
