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

import { Injectable } from '@angular/core';
import { ActivatedRouteSnapshot, Resolve, RouterStateSnapshot } from '@angular/router';
import { Group } from '../models/group';
import { Observable } from 'rxjs';
import { GroupService } from '../services/group.service';
import { APIGetMultiResponse } from '../../services/models/api-response';
import { CollectionParameters } from '../../services/models/api-parameter';
import { map } from 'rxjs/operators';
import { User } from '../models/user';
import { AuthService } from '../../auth/services/auth.service';
import { UserService } from '../services/user.service';

@Injectable({
  providedIn: 'root'
})
export class OwnGroupResolver implements Resolve<Group> {

  constructor(private authService: AuthService, private groupService: GroupService) {
  }

  public resolve(route: ActivatedRouteSnapshot, state: RouterStateSnapshot): Observable<Group> | Promise<Group> | Group {
    const groupID: number = +this.authService.currentUserValue.group_id;
    return this.groupService.getGroup(groupID);
  }
}

/**
 * Resolver for a single group
 */
@Injectable({
  providedIn: 'root'
})
export class GroupResolver implements Resolve<Group> {

  constructor(private groupService: GroupService) {
  }

  public resolve(route: ActivatedRouteSnapshot, state: RouterStateSnapshot): Observable<Group> | Promise<Group> | Group {
    const groupID: number = +route.paramMap.get('publicID');
    return this.groupService.getGroup(groupID);
  }
}

/**
 * Resolver for all groups
 */
@Injectable({
  providedIn: 'root'
})
export class GroupsResolver implements Resolve<Array<Group>> {

  constructor(private groupService: GroupService) {
  }

  public resolve(route: ActivatedRouteSnapshot, state: RouterStateSnapshot):
    Observable<Array<Group>> | Promise<Array<Group>> | Array<Group> {
    const params: CollectionParameters = {
      filter: undefined, limit: 0, sort: 'public_id', order: 1, page: 1
    };
    return this.groupService.getGroups(params).pipe(map((response: APIGetMultiResponse<Group>) => {
      return response.results as Array<Group>;
    }));
  }
}
