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
import {
  AccessControlListEntry,
  AccessControlListSection,
  AccessControlPermission
} from '../../../../../acl/acl.types';
import { Group } from '../../../../../management/models/group';
import { AbstractControl, FormArray, FormControl, FormGroup, Validators } from '@angular/forms';
import { ReplaySubject } from 'rxjs';
import { takeUntil } from 'rxjs/operators';

@Component({
  selector: 'cmdb-groups-acl-tabs',
  templateUrl: './groups-acl-tabs.component.html',
  styleUrls: ['./groups-acl-tabs.component.scss']
})
export class GroupsAclTabsComponent implements OnDestroy {

  /**
   * Component un-subscriber.
   * @private
   */
  private subscriber: ReplaySubject<void> = new ReplaySubject<void>();

  /**
   * Event emitter when a value inside the form changes.
   */
  @Output() public valueChange: EventEmitter<any> = new EventEmitter<any>();

  private _form: FormArray;
  public get form(): FormArray {
    return this._form;
  }

  @Input('form')
  public set Form(arr: FormArray) {
    this._form = arr;
    /*this.form.valueChanges.pipe(takeUntil(this.subscriber)).subscribe(change => {
      this.valueChange.emit(change);
    });*/
  }

  public groupIncludes: Array<AccessControlListEntry<number>>;

  @Input('groupIncludes')
  public set GroupIncludes(includes: Array<AccessControlListEntry<number>>) {
    if (includes) {
      this.groupIncludes = includes;
      for (const entry of this.groupIncludes) {
        this.addEntry();
      }
      this.form.patchValue(includes);
    }
  }

  @Input() public groups: Array<Group>;

  public readonly operations: Array<string> = Object.keys(AccessControlPermission);

  public get controls(): Array<FormGroup> {
    return this.form.controls as Array<FormGroup>;
  }

  /**
   * Is the group already selected
   * @param groupID
   */
  public isGroupSelected(groupID: number): boolean {
    return this.form.controls.some(c => c.get('role').value === groupID);
  }

  /**
   * Add a new acl entry.
   */
  public addEntry(): void {
    const entryGroup = new FormGroup({
      role: new FormControl(undefined, Validators.required),
      permissions: new FormControl([])
    });
    this.form.push(entryGroup);
  }

  /**
   * Remove a existing entry.
   * @param entry
   */
  public removeEntry(entry): void {
    const entryIdx = this.form.controls.indexOf(entry);
    if (entryIdx > -1) {
      this.form.removeAt(entryIdx);
    }
  }

  public ngOnDestroy(): void {
    this.subscriber.next();
    this.subscriber.complete();
  }

}
