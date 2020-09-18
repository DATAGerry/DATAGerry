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

import { AfterViewInit, Component, OnDestroy, OnInit, ViewChild } from '@angular/core';
import { GroupService } from '../../services/group.service';
import { UserService } from '../../services/user.service';
import { DataTableDirective } from 'angular-datatables';
import { forkJoin, Subject, Subscription } from 'rxjs';
import { User } from '../../models/user';
import { Group } from '../../models/group';
import {NgbModal, NgbModalRef} from '@ng-bootstrap/ng-bootstrap';
import { UsersPasswdModalComponent } from '../modals/users-passwd-modal/users-passwd-modal.component';
import { AuthService } from '../../../auth/services/auth.service';
import { NgxSpinnerService } from 'ngx-spinner';

@Component({
  selector: 'cmdb-users-list',
  templateUrl: './users-list.component.html',
  styleUrls: ['./users-list.component.scss']
})
export class UsersListComponent implements OnInit, AfterViewInit, OnDestroy {

  // Display data
  public userList: User[];
  public groupList: Group[];
  private dataSubscription: Subscription;
  private modalRef: NgbModalRef;

  // Table
  private readonly sortingColumnID: number = 1;
  private readonly groupingColumnID: number = 5;
  @ViewChild(DataTableDirective, { static: false })
  private dtElement: DataTableDirective;
  public dtTrigger: Subject<any> = new Subject();
  public readonly dtOptions: any = {
    orderFixed: [this.groupingColumnID, 'asc'],
    rowGroup: {
      enable: true,
      endRender(rows) {
        return `Number of users in this group: ${ rows.count() }`;
      },
      dataSrc: this.groupingColumnID
    },
    ordering: true,
    order: [this.sortingColumnID, 'asc'],
    language: {
      search: '',
      searchPlaceholder: 'Filter...'
    }
  };

  // Current user
  public currentUser: User;

  constructor(private authService: AuthService, private userService: UserService, public groupService: GroupService,
              private modalService: NgbModal, private spinner: NgxSpinnerService) {
    this.dataSubscription = new Subscription();
  }

  public ngOnInit(): void {
    this.spinner.show();
    this.currentUser = this.authService.currentUserValue;
    const dataSubscriptionArray: any[] = [
      this.userService.getUserList(), this.groupService.getGroupList()
    ];
    this.dataSubscription = forkJoin(dataSubscriptionArray).subscribe(
      ([users, groups]) => {
        this.userList = users as [];
        this.groupList = groups as [];
      },
      error => {
        console.error(error);
      },
      () => {
        this.dtTrigger.next();
      }
    ).add(() => this.spinner.hide());
  }

  public ngAfterViewInit(): void {

  }

  public ngOnDestroy(): void {
    this.dataSubscription.unsubscribe();
    this.dtTrigger.unsubscribe();
    if (this.modalRef) {
      this.modalRef.close();
    }
  }

  public findGroup(publicID) {
    return this.groupList.find(g => g.public_id === publicID);
  }

  public openDeleteModal(user: User) {
    this.modalRef = this.modalService.open(UsersPasswdModalComponent, { size: 'lg' });
    this.modalRef.componentInstance.user = user;
  }


}
