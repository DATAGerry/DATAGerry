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

import { Component, OnDestroy, OnInit } from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';
import { GroupService } from '../../services/group.service';
import { Group } from '../../models/group';
import { CollectionParameters } from '../../../services/models/api-parameter';
import { takeUntil } from 'rxjs/operators';
import { pairs, ReplaySubject } from 'rxjs';
import { APIGetMultiResponse } from '../../../services/models/api-response';
import { ToastService } from '../../../layout/toast/toast.service';

@Component({
  selector: 'cmdb-group-acl',
  templateUrl: './group-acl.component.html',
  styleUrls: ['./group-acl.component.scss']
})
export class GroupAclComponent implements OnInit, OnDestroy {

  /**
   * Component unsubscriber.
   * @private
   */
  private subscriber: ReplaySubject<void> = new ReplaySubject<void>();

  /**
   * Group form selector.
   */
  public objectsACLGroupForm: FormGroup;

  /**
   * Chosen group.
   */
  public selectedGroup: Group;

  /**
   * Array of loaded cmdb groups.
   */
  public groups: Array<Group> = [];

  /**
   * Number of group pages.
   * @private
   */
  private totalGroupPages: number;

  /**
   * Total number of groups.
   */
  public totalGroups: number;

  /**
   * ng-select loading indicator.
   */
  public groupsLoading: boolean = false;

  public groupParams: CollectionParameters = {
    filter: undefined, limit: 10, sort: 'public_id', order: 1, page: 1
  };

  constructor(private groupService: GroupService, private toast: ToastService) {
    this.objectsACLGroupForm = new FormGroup({
      group: new FormControl(undefined)
    });
  }

  public get groupControl(): FormControl {
    return this.objectsACLGroupForm.get('group') as FormControl;
  }

  public ngOnInit(): void {
    this.groupsLoading = true;
    this.groupService.getGroups(this.groupParams).pipe(takeUntil(this.subscriber))
      .subscribe((apiResponse: APIGetMultiResponse<Group>) => {
          this.groups = apiResponse.results as Array<Group>;
          this.totalGroups = apiResponse.total;
          this.totalGroupPages = apiResponse.pager.total_pages;
          this.groupsLoading = false;
        },
        (err) => this.toast.error(err)).add(() => this.groupsLoading = false);
    this.groupControl.valueChanges.pipe(takeUntil(this.subscriber)).subscribe((group: Group) => {
      this.selectedGroup = group;
    });
  }

  /**
   * Load more groups until end of list is reached.
   */
  public onScrollToEnd() {
    if (this.groupParams.page < this.totalGroupPages) {
      this.groupParams.page += 1;
      this.loadGroupsFromAPI();
    }
  }

  /**
   * Load the groups from backend.
   * @private
   */
  private loadGroupsFromAPI() {
    this.groupsLoading = true;
    this.groupService.getGroups(this.groupParams).pipe(takeUntil(this.subscriber))
      .subscribe((apiResponse: APIGetMultiResponse<Group>) => {
          this.groups = this.groups.concat(apiResponse.results as Array<Group>);
          this.groupsLoading = false;
        },
        (err) => this.toast.error(err)).add(() => this.groupsLoading = false);
  }

  public ngOnDestroy(): void {
    this.subscriber.next();
    this.subscriber.complete();
  }

}
