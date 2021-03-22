/*
* DATAGERRY - OpenSource Enterprise CMDB
* Copyright (C) 2019 - 2021 NETHINKS GmbH
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

import { Component, Input, OnDestroy, OnInit } from '@angular/core';
import { CmdbType } from '../../models/cmdb-type';
import { TypeService } from '../../services/type.service';
import { UserService } from '../../../management/services/user.service';
import { CmdbMode } from '../../modes.enum';
import { Router } from '@angular/router';
import { ToastService } from '../../../layout/toast/toast.service';
import { Group } from '../../../management/models/group';
import { ReplaySubject } from 'rxjs';
import { User } from '../../../management/models/user';
import { GroupService } from '../../../management/services/group.service';
import { CollectionParameters } from '../../../services/models/api-parameter';
import { takeUntil } from 'rxjs/operators';
import { APIGetMultiResponse } from '../../../services/models/api-response';
import { AccessControlList } from '../../../acl/acl.types';

@Component({
  selector: 'cmdb-type-builder',
  templateUrl: './type-builder.component.html',
  styleUrls: ['./type-builder.component.scss']
})
export class TypeBuilderComponent implements OnInit, OnDestroy {

  private subscriber: ReplaySubject<void> = new ReplaySubject<void>();

  public modes = CmdbMode;
  @Input() public typeInstance?: CmdbType;
  @Input() public mode: CmdbMode = CmdbMode.Create;
  @Input() public stepIndex: number = 0;

  public groups: Array<Group> = [];
  public users: Array<User> = [];

  public basicValid: boolean = true;
  public contentValid: boolean = true;
  public metaValid: boolean = true;
  public accessValid: boolean = true;

  public constructor(private router: Router, private typeService: TypeService, private toast: ToastService,
                     private userService: UserService, private groupService: GroupService) {
  }

  public ngOnInit(): void {
    if (this.mode === CmdbMode.Create) {
      this.typeInstance = new CmdbType();
      this.typeInstance.version = '1.0.0';
      this.typeInstance.author_id = this.userService.getCurrentUser().public_id;
      this.typeInstance.render_meta = {
        icon: undefined,
        sections: [],
        externals: [],
        summary: undefined
      };
      this.typeInstance.acl = new AccessControlList(false);
    }
    const groupsCallParameters: CollectionParameters = {
      filter: undefined,
      limit: 0,
      sort: 'public_id',
      order: 1,
      page: 1
    };
    this.groupService.getGroups(groupsCallParameters).pipe(takeUntil(this.subscriber))
      .subscribe((response: APIGetMultiResponse) => {
        this.groups = [... response.results as Array<Group>];
      });
  }

  public ngOnDestroy(): void {
    this.subscriber.next();
    this.subscriber.complete();
  }

  /*


   public saveType() {
    if (this.mode === CmdbMode.Create) {
      let newTypeID = null;
      this.typeService.postType(this.typeInstance).subscribe((typeIDResp: CmdbType) => {
          newTypeID = +typeIDResp.public_id;
          if (this.selectedCategoryID) {
            this.categoryService.getCategory(this.selectedCategoryID).subscribe((category: CmdbCategory) => {
              category.types.push(newTypeID);
              this.categoryService.updateCategory(category).subscribe(() => {
                this.sidebarService.loadCategoryTree();
                this.router.navigate(['/framework/type/'], { queryParams: { typeAddSuccess: newTypeID } });
              });
            });
          } else {
            this.sidebarService.loadCategoryTree();
            this.router.navigate(['/framework/type/'], { queryParams: { typeAddSuccess: newTypeID } });
          }
          this.toast.success(`Type was successfully created: TypeID: ${ newTypeID }`);
        },
        (error) => {
          console.error(error);
        });
    } else if (this.mode === CmdbMode.Edit) {
      this.typeInstance.creation_time = this.typeInstance.creation_time.$date;
      this.typeService.putType(this.typeInstance).subscribe((updateResp: CmdbType) => {
          if (this.basicStep.originalCategoryID !== this.selectedCategoryID) {
            // Remove from old category
            if (this.basicStep.originalCategoryID) {
              this.categoryService.getCategory(this.basicStep.originalCategoryID).subscribe((category: CmdbCategory) => {
                const index = category.types.indexOf(this.typeInstance.public_id, 0);
                if (index > -1) {
                  category.types.splice(index, 1);
                }
                this.categoryService.updateCategory(category).subscribe(() => {
                });
              });
            }
            // Add to new category
            if (this.selectedCategoryID) {
              this.categoryService.getCategory(this.selectedCategoryID).subscribe((category: CmdbCategory) => {
                category.types.push(this.typeInstance.public_id);
                this.categoryService.updateCategory(category).subscribe(() => {
                });
              });
            }
          }
          this.sidebarService.loadCategoryTree();
          this.toast.success(`Type was successfully edited: TypeID: ${ updateResp.public_id }`);
          this.router.navigate(['/framework/type/'], { queryParams: { typeEditSuccess: updateResp.public_id } });
        },
        (error) => {
          console.log(error);
        });
    }
  }

 */

}
