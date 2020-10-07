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
import { Subject } from 'rxjs';
import { Group } from '../../models/group';
import { ActivatedRoute, Data } from '@angular/router';
import { GroupFormComponent } from '../components/group-form/group-form.component';

@Component({
  selector: 'cmdb-group-edit',
  templateUrl: './group-edit.component.html',
  styleUrls: ['./group-edit.component.scss']
})
export class GroupEditComponent implements OnInit, OnDestroy {

  @ViewChild(GroupFormComponent, {static: true}) private groupForm: GroupFormComponent;
  private unSubscriber: Subject<void> = new Subject<void>();

  public group: Group;

  constructor(private route: ActivatedRoute, private groupService: GroupService) {
  }

  public ngOnInit(): void {
    this.group = this.route.snapshot.data.group as Group;
    this.groupForm.nameControl.clearAsyncValidators();
  }

  public ngOnDestroy(): void {
    this.unSubscriber.next();
    this.unSubscriber.complete();
  }

  public submit(group: Group): void {
  }

}
