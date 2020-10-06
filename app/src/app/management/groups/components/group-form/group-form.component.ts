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
* along with this program. If not, see <https://www.gnu.org/licenses/>.
*/

import { Component, EventEmitter, Input, OnDestroy, OnInit, Output } from '@angular/core';
import { Group } from '../../../models/group';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { Subject } from 'rxjs';
import { takeUntil } from 'rxjs/operators';
import { groupNameExistsValidator, GroupService } from '../../../services/group.service';
import { RightService } from '../../../services/right.service';
import { Right } from '../../../models/right';
import { APIGetMultiResponse } from '../../../../services/models/api-response';
import { CollectionParameters } from '../../../../services/models/api-parameter';

@Component({
  selector: 'cmdb-group-form',
  templateUrl: './group-form.component.html',
  styleUrls: ['./group-form.component.scss']
})
export class GroupFormComponent implements OnInit, OnDestroy {

  private subscriber: Subject<void>;
  public form: FormGroup;

  /**
   * Passable group data if there are pre data.
   */
  @Input() public group: Group;

  /**
   * Validation status event emitter.
   */
  @Output() public validation: EventEmitter<boolean>;

  /**
   * Form submit event emitter.
   */
  @Output() public submit: EventEmitter<Group>;

  /**
   * Current right list
   */
  public rights: Array<Right> = [];
  private currentRightPage: number = 1;
  private totalRightPage: number = -1;

  constructor(private groupService: GroupService, private rightService: RightService) {
    this.subscriber = new Subject<void>();
    this.validation = new EventEmitter<boolean>();
    this.submit = new EventEmitter<Group>();
    this.form = new FormGroup({
      name: new FormControl('', [Validators.required],
        [groupNameExistsValidator(this.groupService)]),
      label: new FormControl('', [Validators.required]),
      rights: new FormControl([])
    });
  }

  /**
   * Init for group form component.
   * Subscribes to status changes.
   */
  public ngOnInit(): void {
    this.form.statusChanges.pipe(takeUntil(this.subscriber)).subscribe(status => {
      this.validation.emit(status);
    });
    this.loadRights(this.currentRightPage);
  }

  public onScrollToEnd() {
    this.loadRights(this.currentRightPage + 1);
  }

  private loadRights(page: number): void {
    if (page !== this.totalRightPage) {
      this.rightService.getRights({
        filter: undefined,
        limit: 10,
        sort: 'name',
        order: 1,
        page
      }).pipe(takeUntil(this.subscriber))
        .subscribe((apiResponse: APIGetMultiResponse<Right>) => {
          this.currentRightPage = +apiResponse.pager.page;
          console.log(this.currentRightPage);
          this.totalRightPage = +apiResponse.pager.total_pages;
          console.log(this.totalRightPage);
          this.rights.push(...apiResponse.results as Array<Right>);
          console.log(this.rights);
        });
    }
  }

  /**
   * Get the form control for name.
   */
  public get name(): FormControl {
    return this.form.get('name') as FormControl;
  }

  /**
   * Get the form control for label.
   */
  public get label(): FormControl {
    return this.form.get('label') as FormControl;
  }

  /**
   * Get the rights array control.
   */
  public get rightsControl(): FormControl {
    return this.form.get('rights') as FormControl;
  }

  /**
   * Calls on ngSubmit of the form.
   * Triggers the submit event emitter.
   */
  public onSubmit(): void {
    const formGroup: Group = this.form.getRawValue() as Group;
    this.group = { ...this.group, ...formGroup };
    return this.submit.emit(formGroup);
  }

  /**
   * Destroys the component.
   * Calls the auto unsubscriber.
   */
  public ngOnDestroy(): void {
    this.subscriber.next();
    this.subscriber.complete();
  }

}
