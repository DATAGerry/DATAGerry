import { Injectable } from '@angular/core';
import {CmdbType} from '../../framework/models/cmdb-type';
import {AuthService} from './auth.service';

@Injectable({
  providedIn: 'root'
})
export class AclPermissionService {

  private type: CmdbType;
  private readonly currentGroup: number;

  constructor(private authService: AuthService) {
    this.currentGroup = this.authService.currentUserValue.group_id;
  }

  public checkRights(type: CmdbType, rights: string | string[]) {
    if (!type.acl.activated) {
      return true;
    }
    this.type = type;
    if (Array.isArray(rights)) {
      for (const right in rights) {
        if (!this.hasRight(right)) {
          return false;
        }
      }
    } else {
      if (!this.hasRight((rights))) {
        return false;
      }
    }
    return true;
  }

  private hasRight(right: string) {
    const rights = this.type.acl.groups.includes[this.currentGroup] as string[];
    console.log(rights);
    if (rights.includes(right)) {
      return true;
    }
    return false;
  }

}
