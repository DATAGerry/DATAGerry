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

import { Component, OnDestroy, OnInit } from '@angular/core';
import { Group } from '../../models/group';
import { ActivatedRoute, Router } from '@angular/router';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { GroupService } from '../../services/group.service';
import { takeUntil } from 'rxjs/operators';
import { ReplaySubject } from 'rxjs';
import { ToastService } from '../../../layout/toast/toast.service';

@Component({
  selector: 'cmdb-group-delete',
  templateUrl: './group-delete.component.html',
  styleUrls: ['./group-delete.component.scss']
})
export class GroupDeleteComponent implements OnDestroy{

  public group: Group;
  public groups: Array<Group> = [];
  public deleteForm: FormGroup;

  private subscriber: ReplaySubject<void> = new ReplaySubject<void>();

  constructor(private route: ActivatedRoute, private router: Router, private groupService: GroupService,
              private toast: ToastService) {
    this.group = this.route.snapshot.data.group as Group;
    this.groups = this.route.snapshot.data.groups as Array<Group>;

    this.deleteForm = new FormGroup({
      deleteGroupAction: new FormControl('', Validators.required),
      deleteGroupOption: new FormControl(2)
    });
  }

  /**
   * On group deletion
   */
  public delete() {
    if (this.deleteForm.valid) {
      const action = this.deleteForm.get('deleteGroupAction').value;
      const groupID = this.deleteForm.get('deleteGroupOption').value;
      this.groupService.deleteGroup(this.group.public_id, action, groupID).pipe(takeUntil(this.subscriber)).subscribe(() => {
        this.toast.success(`Group ${ this.group.label } was deleted`);
        this.router.navigate(['/', 'management', 'groups']);
      });
    }
  }

  /**
   * Auto unsubscribe on component destroy.
   */
  public ngOnDestroy(): void {
    this.subscriber.next();
    this.subscriber.complete();
  }

}
