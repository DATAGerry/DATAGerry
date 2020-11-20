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


import { Directive, ElementRef, Input, TemplateRef, ViewContainerRef } from '@angular/core';
import { PermissionService } from '../services/permission.service';
import {CmdbType} from '../../framework/models/cmdb-type';
import {AclPermissionService} from '../services/acl-permission.service';

@Directive({
  // tslint:disable-next-line:directive-selector
  selector: '[permissionLink]',
  exportAs: 'permissionLink'
})
export class PermissionLinkDirective {

  private rightNames: string[] = [];
  private acl: string[] | string = undefined;
  private type: CmdbType = undefined;

  constructor(private element: ElementRef,
              private templateRef: TemplateRef<any>,
              private viewContainer: ViewContainerRef, private permissionService: PermissionService,
              private aclPermissionService: AclPermissionService) {
  }

  @Input('permissionLinkAcl') set permissionLinkAcl(acl: string | string[]) {
    this.acl = acl;
  }

  @Input('permissionLinkType') set permissionLinkType(type: CmdbType) {
    this.type = type;
  }

  @Input('permissionLink') set permissionLink(rightNames: string | string[]) {
    if (rightNames !== undefined) {
      if (Array.isArray(rightNames)) {
        this.rightNames = rightNames;
      } else {
        this.rightNames = [];
        this.rightNames.push(rightNames);
      }
      this.updateView();
    }
  }

  @Input() routerLink: string = undefined;

  private checkPermission() {
    let hasPermission = false;
    for (const right of this.rightNames) {
      if (this.permissionService.hasRight(right)) {
        hasPermission = true;
        break;
      } else if (this.permissionService.hasExtendedRight(right)) {
        hasPermission = true;
      }
    }

    if (this.type && this.acl && hasPermission) {
      const aclperms = this.aclPermissionService.checkRights(this.type, this.acl);
      if (aclperms !== null) {
        hasPermission = aclperms;
      }
    }

    return hasPermission;
  }

  private updateView() {
    if (this.checkPermission()) {
      this.viewContainer.createEmbeddedView(this.templateRef);
    } else {
      this.viewContainer.clear();
    }
  }

}
