/*
* dataGerry - OpenSource Enterprise CMDB
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

import { Component, Input, OnInit, ViewChild } from '@angular/core';
import { TypeBasicStepComponent } from './type-basic-step/type-basic-step.component';
import { CmdbType } from '../../../models/cmdb-type';
import { TypeFieldsStepComponent } from './type-fields-step/type-fields-step.component';
import { TypeMetaStepComponent } from './type-meta-step/type-meta-step.component';
import { TypeAccessStepComponent } from './type-access-step/type-access-step.component';
import { TypeService } from '../../../services/type.service';
import { UserService } from '../../../../user/services/user.service';
import { CategoryService } from '../../../services/category.service';
import { CmdbMode } from '../../../modes.enum';
import { Router } from '@angular/router';
import { ToastService } from '../../../../layout/services/toast.service';


@Component({
  selector: 'cmdb-type-builder',
  templateUrl: './type-builder.component.html',
  styleUrls: ['./type-builder.component.scss']
})
export class TypeBuilderComponent implements OnInit {


  @Input() public typeInstance?: CmdbType;
  @Input() public mode: number = CmdbMode.Create;

  @ViewChild(TypeBasicStepComponent, {static: true})
  public basicStep: TypeBasicStepComponent;

  @ViewChild(TypeFieldsStepComponent, {static: true})
  public fieldStep: TypeFieldsStepComponent;

  @ViewChild(TypeMetaStepComponent, {static: true})
  public metaStep: TypeMetaStepComponent;

  @ViewChild(TypeAccessStepComponent, {static: true})
  public accessStep: TypeAccessStepComponent;

  public selectedCategoryID: number = 0;

  public constructor(private router: Router, private typeService: TypeService, private toast: ToastService,
                     private userService: UserService, private categoryService: CategoryService) {

  }

  public ngOnInit(): void {
    if (this.mode === CmdbMode.Create) {
      this.typeInstance = new CmdbType();
      this.typeInstance.version = '1.0.0';
      this.typeInstance.author_id = this.userService.getCurrentUser().public_id;
    }
  }

  public exitBasicStep() {
    this.selectedCategoryID = this.basicStep.basicCategoryForm.value.category_id;
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
    this.assignToType({fields: fieldBuffer});
    this.assignToType({sections: sectionBuffer}, 'render_meta');
  }

  public exitMetaStep() {
    this.assignToType({summary: this.metaStep.summariesSections}, 'render_meta');
    this.assignToType({external: this.metaStep.externalLinks}, 'render_meta');
  }

  public exitAccessStep() {
    this.assignToType(this.accessStep.accessForm.value, 'access');
  }

  public saveType() {

    if (this.mode === CmdbMode.Create) {
      let newTypeID = null;
      this.typeService.postType(this.typeInstance).subscribe(typeIDResp => {
          newTypeID = typeIDResp;

          const selectedCategory = this.categoryService.findCategory(this.selectedCategoryID);
          selectedCategory.type_list.push(newTypeID);
          this.categoryService.updateCategory(selectedCategory).subscribe((ack: number) => {
            this.router.navigate(['/framework/type/'], {queryParams: {typeAddSuccess: newTypeID}});
          });

        },
        (error) => {
          console.error(error);
        });
    } else if (this.mode === CmdbMode.Edit) {
      this.typeService.putType(this.typeInstance).subscribe((updateResp: CmdbType) => {
          this.toast.show(`Type was successfully edit: TypeID: ${updateResp.public_id}`);
          this.router.navigate(['/framework/type/'], {queryParams: {typeEditSuccess: updateResp.public_id}});
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
  }

}
