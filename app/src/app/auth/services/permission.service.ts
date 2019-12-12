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

import { Injectable } from '@angular/core';
import { Right } from '../../management/models/right';
import { BehaviorSubject, Observable } from 'rxjs';
import { GroupService } from '../../management/services/group.service';
import { Group } from '../../management/models/group';
import { first, map } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class PermissionService {

  // Right storage
  private currentUserRightListSubject: BehaviorSubject<string[]>;
  public currentUserRightList: Observable<string[]>;

  constructor(private groupService: GroupService) {
    this.currentUserRightListSubject = new BehaviorSubject<string[]>(
      JSON.parse(localStorage.getItem('current-user-rights')));
    this.currentUserRightList = this.currentUserRightListSubject.asObservable();
  }

  public get currentUserRights(): string[] {
    if (this.currentUserRightListSubject.value == null) {
      return [];
    }
    return this.currentUserRightListSubject.value;
  }

  public storeUserRights(groupID: number) {
    return this.groupService.getGroup(groupID).pipe(map(
      group => {
        localStorage.setItem('current-user-rights', JSON.stringify(group.rights));
        this.currentUserRightListSubject.next(group.rights);
        return group;
      }
    ));
    /*return this.groupService.getGroup(groupID).pipe(first()).subscribe(
      (group: Group) => {
        localStorage.setItem('current-user-rights', JSON.stringify(group.rights));
        this.currentUserRightListSubject.next(group.rights);
        resolve("test");
      },
      (error) => console.error(error)
    );*/
  }

  public clearUserRightStorage() {
    localStorage.removeItem('current-user-rights');
    this.currentUserRightListSubject.next(null);
  }

  public hasRight(rightName: string): boolean {
    return !!this.currentUserRights.find(right => right === rightName);
  }

  public hasExtendedRight(rightName: string): boolean {
    let status = false;
    rightName = rightName.substring(0, rightName.lastIndexOf('.'));
    if (this.hasRight(`${ rightName }.*`)) {
      status = true;
    } else {
      if (rightName === 'base') {
        return false;
      }
      status = this.hasExtendedRight(rightName);
    }
    return status;
  }
}
