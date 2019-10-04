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
import { GroupService } from '../../services/group.service';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { RightService } from '../../services/right.service';
import { Right } from '../../models/right';
import { ToastService } from '../../../layout/services/toast.service';
import { ActivatedRoute, Router } from '@angular/router';
import { Observable, Subscription } from 'rxjs';
import { Group } from '../../models/group';

@Component({
  selector: 'cmdb-groups-add',
  templateUrl: './groups-add.component.html',
  styleUrls: ['./groups-add.component.scss']
})
export class GroupsAddComponent implements OnInit, OnDestroy {

  private rightServiceSubscription: Subscription;

  public rightList: Right[];
  public addGroup: Group;
  public addForm: FormGroup;

  constructor(private groupService: GroupService, private rightService: RightService,
              private toast: ToastService, private router: Router) {
    this.addForm = new FormGroup({
      name: new FormControl('', Validators.required),
      label: new FormControl(''),
      rights: new FormControl([], Validators.minLength(1))
    });
  }

  public ngOnInit(): void {
    this.rightServiceSubscription = this.rightService.getRightList().subscribe((rightList: Right[]) => {
      this.rightList = rightList;
    });
  }

  public groupByFn(item) {
    const baseData = item.name.split('.');
    return `${ baseData[0] }.${ baseData[1] }.*`;
  }

  public get name() {
    return this.addForm.get('name');
  }

  public get label() {
    return this.addForm.get('label');
  }

  public get rights() {
    return this.addForm.get('rights');
  }

  public ngOnDestroy(): void {
    this.rightServiceSubscription.unsubscribe();
  }

  public saveGroup() {
    const rawData = this.addForm.getRawValue();
    if (this.addForm.valid) {
      this.groupService.postGroup(rawData).subscribe(insertAck => {
          this.toast.show(`Group was added with ID: ${ insertAck }`);
        },
        (error) => {
          console.error(error);
        }, () => {
          this.router.navigate(['/management/groups/']);
        });
    }

  }

}
