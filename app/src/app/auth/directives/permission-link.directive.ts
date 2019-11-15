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

@Directive({
  // tslint:disable-next-line:directive-selector
  selector: '[permissionLink]',
  exportAs: 'permissionLink'
})
export class PermissionLinkDirective {

  private displayRightName: string = undefined;

  constructor(private element: ElementRef,
              private templateRef: TemplateRef<any>,
              private viewContainer: ViewContainerRef, private permissionService: PermissionService) {
  }

  @Input('permissionLink') set permissionLink(rightName: string) {
    if (rightName !== undefined) {
      this.displayRightName = rightName;
      this.updateView();
    }
  }

  @Input() routerLink: string = undefined;

  private checkPermission() {
    let hasPermission = false;
    if (this.permissionService.hasRight(this.displayRightName)) {
      hasPermission = true;
    } else if (this.permissionService.hasExtendedRight(this.displayRightName)) {
      hasPermission = true;
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
