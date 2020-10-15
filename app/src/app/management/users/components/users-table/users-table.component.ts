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

import { Component, Input, OnDestroy } from '@angular/core';
import { User } from '../../../models/user';
import { GroupService } from '../../../services/group.service';
import { Group } from '../../../models/group';
import { NgbModal, NgbModalRef } from '@ng-bootstrap/ng-bootstrap';
import { UsersPasswdModalComponent } from '../../modals/users-passwd-modal/users-passwd-modal.component';


@Component({
  selector: 'cmdb-users-table',
  templateUrl: './users-table.component.html',
  styleUrls: ['./users-table.component.scss']
})
export class UsersTableComponent implements OnDestroy{

  /**
   * Password modal
   */
  private modalRef: NgbModalRef;

  /**
   * User list
   */
  @Input() public users: Array<User> = [];

  /**
   * Group list
   */
  @Input() public groups: Array<Group> = [];

  /**
   * Datatable
   */
  @Input() public tableOptions: any = {};

  constructor(public groupService: GroupService, private modalService: NgbModal) {
  }

  public findGroup(groupID: number): Group {
    return this.groups.find(g => g.public_id === groupID);
  }

  public openPasswordModal(user: User) {
    this.modalRef = this.modalService.open(UsersPasswdModalComponent, { size: 'lg' });
    this.modalRef.componentInstance.user = user;
  }

  public ngOnDestroy(): void {
    this.modalRef.close();
  }

}
