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

import { Component, Input, OnDestroy, OnInit } from '@angular/core';
import { CmdbType } from '../../../models/cmdb-type';
import { FormControl, FormGroup } from '@angular/forms';
import { ReplaySubject } from 'rxjs';
import { takeUntil } from 'rxjs/operators';
import { AccessControlList } from '../../../../acl/acl.types';

@Component({
  selector: 'cmdb-type-acl-step',
  templateUrl: './type-acl-step.component.html',
  styleUrls: ['./type-acl-step.component.scss']
})
export class TypeAclStepComponent implements OnInit, OnDestroy {

  private subscriber: ReplaySubject<void> = new ReplaySubject<void>();

  public acl: AccessControlList;

  @Input() public type: CmdbType;
  public form: FormGroup;

  constructor() {
    this.acl = new AccessControlList(false);
    this.form = new FormGroup({
      activated: new FormControl(false),
      groups: new FormGroup({
        activated: new FormControl(false),
      })
    });
  }

  public get activatedControl(): FormControl {
    return this.form.get('activated') as FormControl;
  }

  public get groupsControl(): FormGroup {
    return this.form.get('groups') as FormGroup;
  }

  public ngOnInit(): void {
    this.groupsControl.valueChanges.pipe(takeUntil(this.subscriber)).subscribe(changes => {
      if (changes.activated) {
        this.activatedControl.setValue(true);
      }
    });
  }

  public ngOnDestroy(): void {
    this.subscriber.next();
    this.subscriber.complete();
  }

}
