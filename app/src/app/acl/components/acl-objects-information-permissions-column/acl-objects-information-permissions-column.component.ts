/*
* DATAGERRY - OpenSource Enterprise CMDB
* Copyright (C) 2024 becon GmbH
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

import { Component, Input, OnChanges, SimpleChanges } from '@angular/core';
import { AccessControlList, AccessControlPermission } from '../../acl.types';
import { Group } from '../../../management/models/group';

@Component({
  selector: 'cmdb-acl-objects-information-permissions-column',
  templateUrl: './acl-objects-information-permissions-column.component.html',
  styleUrls: ['./acl-objects-information-permissions-column.component.scss']
})
export class AclObjectsInformationPermissionsColumnComponent implements OnChanges {

  /**
   * Selected group which compares to the acl.
   */
  @Input() public group: Group;

  /**
   * ACL of the current row type.
   */
  @Input() public acl: AccessControlList;

  public permissions: Array<AccessControlPermission> = [];


  public generate(): void {
    if (!this.group || !this.acl) {
      this.permissions = [];
    } else {
      const groupID: number = this.group.public_id;
      if (groupID in this.acl.groups.includes) {
        this.permissions = this.acl.groups.includes[groupID];
      }
    }
  }

  public ngOnChanges(changes: SimpleChanges): void {
    this.generate();
  }

}
