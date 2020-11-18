import { Injectable } from '@angular/core';
import {CmdbType} from '../../framework/models/cmdb-type';
import {AuthService} from './auth.service';

@Injectable({
  providedIn: 'root'
})
export class AclPermissionService {

  private type: CmdbType;
  private currentGroup: number;

  constructor(private authService: AuthService) {
    this.currentGroup = this.authService.currentUserValue.group_id;
  }

  public hasrights(type: CmdbType, rights: string | string[]) {
    if (!type.acl.activated) {
      return true;
    }
    if (Array.isArray(rights)) {
      for (const right in rights) {
        // TODO make this work an a legit model
        if (!(right in type.acl.groups[this.currentGroup].permissions)) {
          return false;
        }
      }
    } else {
      if (!(rights in type.acl.groups[this.currentGroup].permissions)) {
        return false;
      }
    }

    return true;

  }

}
