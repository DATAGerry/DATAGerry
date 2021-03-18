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
import { CmdbCategory } from '../../models/cmdb-category';
import { Group } from '../../../management/models/group';
import { ReplaySubject } from 'rxjs';
import { User } from '../../../management/models/user';

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
  public categories: Array<CmdbCategory> = [];

  public constructor(private router: Router, private typeService: TypeService,
                     private toast: ToastService, private userService: UserService){
  }

  public ngOnInit(): void {
    if (this.mode === CmdbMode.Create) {
      this.typeInstance = new CmdbType();
      this.typeInstance.version = '1.0.0';
      this.typeInstance.author_id = this.userService.getCurrentUser().public_id;
      this.typeInstance.render_meta = {
        sections: [],
        externals: []
      };
    }
  }

  public ngOnDestroy(): void {
    this.subscriber.next();
    this.subscriber.complete();
  }

  /*
   public exitBasicStep() {
    this.selectedCategoryID = this.basicStep.basicCategoryForm.value.category_id;
    const defaultIcon = this.basicStep.basicMetaIconForm.get('icon').value === '' ?
      'fas fa-cube' : this.basicStep.basicMetaIconForm.get('icon').value;
    this.assignToType({ icon: defaultIcon }, 'render_meta');
    this.assignToType(this.basicStep.basicForm.value);
  }

   public exitFieldStep() {
    let fieldBuffer = [];
    let sectionBuffer = [];
    const sectionOrigin = this.fieldStep.typeBuilder.sections;
    for (const section of sectionOrigin) {
      const sectionGlobe = Object.assign({}, section);
      fieldBuffer = fieldBuffer.concat(sectionGlobe.fields);
      const sectionFieldNames = new Set(sectionGlobe.fields.map(f => f.name));
      delete sectionGlobe.fields;

      sectionGlobe.fields = Array.from(sectionFieldNames);

      sectionBuffer = sectionBuffer.concat(sectionGlobe);
    }
    this.assignToType({ fields: fieldBuffer });
    this.assignToType({ sections: sectionBuffer }, 'render_meta');
  }

   public exitMetaStep() {
    this.assignToType({ summary: this.metaStep.summaryForm.getRawValue() }, 'render_meta');
    this.assignToType({ externals: this.metaStep.externalLinks }, 'render_meta');
  }

   public exitAccessStep() {
    this.assignToType({ acl: this.aclStep.form.getRawValue() });
  }

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

   public assignToType(data: any, optional: any = null) {
    if (optional !== null) {
      if (this.typeInstance[optional] === undefined) {
        this.typeInstance[optional] = {};
      }
      Object.assign(this.typeInstance[optional], data);
    } else {
      Object.assign(this.typeInstance, data);
    }
  }*/

}
