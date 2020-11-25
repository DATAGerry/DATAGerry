import { Injectable } from '@angular/core';
import {CmdbType} from '../../framework/models/cmdb-type';
import {AuthService} from './auth.service';
import {AccessControlList} from "../../acl/acl.types";

@Injectable({
  providedIn: 'root'
})
export class AclPermissionService {

  private acl: AccessControlList;
  private readonly currentGroup: number;

  constructor(private authService: AuthService) {
    this.currentGroup = this.authService.currentUserValue.group_id;
  }

  public checkRights(acl: AccessControlList, rights: string | string[]) {
    if (!acl.activated) {
      return null;
    }
    this.acl = acl;
    if (Array.isArray(rights)) {

      if (rights.length === 1) {
        return this.hasRight(rights[0]);
      }

      for (const right of rights) {
        if (!this.hasRight(right)) {
          return false;
        }
      }
    } else {
      return this.hasRight(rights);
    }
    return true;
  }

  private hasRight(right: string) {
    const rights = this.acl.groups.includes[this.currentGroup] as string[];
    if (!rights) {
      return false;
    }
    return rights.includes(right);

  }

}
