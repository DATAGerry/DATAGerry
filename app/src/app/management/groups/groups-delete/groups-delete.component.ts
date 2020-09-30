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
import { Observable, Subscription } from 'rxjs';
import { Group } from '../../models/group';
import { GroupService } from '../../services/group.service';
import { ActivatedRoute, Router } from '@angular/router';
import { ToastService } from '../../../layout/toast/toast.service';
import { FormControl, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'cmdb-groups-delete',
  templateUrl: './groups-delete.component.html',
  styleUrls: ['./groups-delete.component.scss']
})
export class GroupsDeleteComponent implements OnInit, OnDestroy {

  private readonly defaultOptionSelection: number = 2;

  public groupID: number;
  private routeParamObserver: Observable<any>;
  private routeParamSubscription: Subscription;
  private groupServiceObserver: Observable<Group>;
  private groupServiceSubscription: Subscription;
  private groupListSubscription: Subscription;

  public deleteAbleGroup: Group;
  public groupList: Group[];
  public deleteForm: FormGroup;

  constructor(private groupService: GroupService, private route: ActivatedRoute,
              private toast: ToastService, private router: Router) {
    this.routeParamSubscription = new Subscription();
    this.groupServiceSubscription = new Subscription();
    this.groupListSubscription = new Subscription();
    this.routeParamObserver = this.route.params;
    this.deleteForm = new FormGroup({
      deleteGroupAction: new FormControl('', Validators.required),
      deleteGroupOption: new FormControl(this.defaultOptionSelection)
    });
  }

  public ngOnInit(): void {
    this.routeParamSubscription = this.routeParamObserver.subscribe(
      (params) => {
        this.groupID = params.publicID;
        this.groupServiceObserver = this.groupService.getGroup(this.groupID);
        this.groupServiceSubscription = this.groupService.getGroup(this.groupID).subscribe((group: Group) => {
          this.deleteAbleGroup = group;
        });
      }
    );
    this.groupListSubscription = this.groupService.getGroups().subscribe((groupList: Group[]) => {
      this.groupList = groupList;
      this.deleteForm.get('deleteGroupOption').setValue(2);
    });
  }

  public onDeleteGroup(): void {
    if (this.deleteForm.valid) {
      const groupDeleteSub = this.groupService.deleteGroup(this.groupID, this.deleteForm.get('deleteGroupAction').value,
        {group_id: this.deleteForm.get('deleteGroupOption').value})
        .subscribe(ack => {
            if (ack) {
              this.toast.success('Group was deleted');
              this.router.navigate(['/management/groups/']);
            }
          },
          error => {
            console.error(error);
          },
          () => {
            groupDeleteSub.unsubscribe();
          }
        );
    }
  }

  public ngOnDestroy(): void {
    this.routeParamSubscription.unsubscribe();
    this.groupServiceSubscription.unsubscribe();
    this.groupListSubscription.unsubscribe();
  }

}
