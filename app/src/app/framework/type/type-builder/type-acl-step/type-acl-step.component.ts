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

import { Component, EventEmitter, Input, OnDestroy, OnInit, Output } from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';
import { ReplaySubject } from 'rxjs';
import { takeUntil } from 'rxjs/operators';
import { Group } from '../../../../management/models/group';
import { AccessControlList } from '../../../../acl/acl.types';

@Component({
  selector: 'cmdb-type-acl-step',
  templateUrl: './type-acl-step.component.html',
  styleUrls: ['./type-acl-step.component.scss']
})
export class TypeAclStepComponent implements OnInit, OnDestroy {

  private subscriber: ReplaySubject<void> = new ReplaySubject<void>();
  public acl: AccessControlList;
  private wasEmpty: boolean = true;

  @Input('acl')
  public set ACL(access: AccessControlList) {
    if (access) {
      this.acl = access;
      this.form.patchValue(this.acl);
    }
  }

  @Input() public groups: Array<Group> = [];
  @Output() public validStatus: EventEmitter<boolean> = new EventEmitter<boolean>();
  @Output() public isEmpty: EventEmitter<boolean> = new EventEmitter<boolean>();

  public form: FormGroup;

  constructor() {
    this.form = new FormGroup({
      activated: new FormControl(false),
      groups: new FormGroup({
        includes: new FormGroup({})
      })
    });
  }



  public get activatedStatus(): boolean {
    return this.form.get('activated').value;
  }

  public get groupsControl(): FormGroup {
    return this.form.get('groups') as FormGroup;
  }

  public get includesControl(): FormGroup {
    return this.groupsControl.get('includes') as FormGroup;
  }

  public onAddChange(event) {
    this.wasEmpty = (!event[0] || event[0].length === 0) && !event[1];
    this.isEmpty.emit(this.wasEmpty);
  }

  public ngOnInit(): void {
    this.form.statusChanges.pipe(takeUntil(this.subscriber)).subscribe((status) => {
      if (!this.form.get('activated').value) {
        this.isEmpty.emit(true);
        this.validStatus.emit(true);
      } else {
        this.isEmpty.emit(this.wasEmpty);
        this.validStatus.emit(this.form.valid);
      }
    });
  }

  public ngOnDestroy(): void {
    this.subscriber.next();
    this.subscriber.complete();
  }

}
