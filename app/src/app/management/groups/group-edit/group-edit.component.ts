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

import { Component, OnDestroy, OnInit, ViewChild } from '@angular/core';
import { GroupService } from '../../services/group.service';
import { ReplaySubject, Subject } from 'rxjs';
import { Group } from '../../models/group';
import { ActivatedRoute, Data, Router } from '@angular/router';
import { GroupFormComponent } from '../components/group-form/group-form.component';
import { Right } from '../../models/right';
import { takeUntil } from 'rxjs/operators';
import { ToastService } from '../../../layout/toast/toast.service';

@Component({
  selector: 'cmdb-group-edit',
  templateUrl: './group-edit.component.html',
  styleUrls: ['./group-edit.component.scss']
})
export class GroupEditComponent implements OnInit, OnDestroy {

  @ViewChild(GroupFormComponent, { static: true }) private groupForm: GroupFormComponent;

  public rights: Array<Right> = [];
  public valid: boolean = false;
  private subscriber: ReplaySubject<void> = new ReplaySubject<void>();
  public group: Group;

  constructor(private route: ActivatedRoute, private router: Router, private groupService: GroupService,
              private toastService: ToastService) {
    this.rights = this.route.snapshot.data.rights as Array<Right>;
    this.group = this.route.snapshot.data.group as Group;
  }

  public ngOnInit(): void {
    this.group = this.route.snapshot.data.group as Group;
    this.groupForm.nameControl.clearAsyncValidators();
    this.groupForm.nameControl.disable();
  }

  public ngOnDestroy(): void {
    this.subscriber.next();
    this.subscriber.complete();
  }

  public edit(group: Group): void {
    const editGroup = Object.assign(this.group, group);
    if (this.valid) {
      this.groupService.putGroup(this.group.public_id, editGroup).pipe(takeUntil(this.subscriber)).subscribe((g: Group) => {
          this.toastService.success(`Group ${g.label} was updated!`);
          this.router.navigate(['/', 'management', 'groups']);
        }
      );
    }
  }

}
