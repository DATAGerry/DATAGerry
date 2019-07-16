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

import { Component, OnDestroy, OnInit, ViewChild } from '@angular/core';
import { TypeService } from '../../services/type.service';
import { CmdbType } from '../../models/cmdb-type';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { BehaviorSubject, Observable } from 'rxjs';
import { CmdbMode } from '../../modes.enum';
import { RenderComponent } from '../../render/render.component';
import { CmdbObject } from '../../models/cmdb-object';
import { UserService } from '../../../user/services/user.service';
import { ObjectService } from '../../services/object.service';
import { Router } from '@angular/router';

@Component({
  selector: 'cmdb-object-add',
  templateUrl: './object-add.component.html',
  styleUrls: ['./object-add.component.scss']
})
export class ObjectAddComponent implements OnInit, OnDestroy {

  public typeList: CmdbType[];
  public typeIDForm: FormGroup;
  private typeIDSubject: BehaviorSubject<number>;
  public typeID: Observable<number>;
  public typeInstance: CmdbType;
  public mode: CmdbMode = CmdbMode.Create;
  public objectInstance: CmdbObject;
  @ViewChild(RenderComponent, {static: false}) render: RenderComponent;


  constructor(private router: Router, private typeService: TypeService, private objectService: ObjectService, private userService: UserService) {
    this.objectInstance = new CmdbObject();
    this.typeIDSubject = new BehaviorSubject<number>(null);
    this.typeID = this.typeIDSubject.asObservable();
    this.typeID.subscribe(selectedTypeID => {
      if (selectedTypeID !== null) {
        this.typeService.getType(selectedTypeID).subscribe((typeInstance: CmdbType) => {
          this.typeInstance = typeInstance;
        });
      }
    });
  }

  public ngOnInit(): void {
    this.typeService.getTypeList().subscribe((typeList: CmdbType[]) => {
      this.typeList = typeList;
    });
    this.typeIDForm = new FormGroup({
      typeID: new FormControl(null, Validators.required)
    });
  }

  public ngOnDestroy(): void {
    this.typeIDSubject.unsubscribe();
  }

  public get formTypeID() {
    return this.typeIDForm.get('typeID').value;
  }

  public useTypeID() {
    this.typeIDSubject.next(this.formTypeID);
  }

  public get currentTypeID() {
    return this.typeIDSubject.value;
  }

  public saveObject() {
    this.objectInstance.type_id = this.currentTypeID;
    this.objectInstance.active = this.render.renderForm.get('active').value;
    this.objectInstance.version = '1.0.0';
    this.objectInstance.author_id = this.userService.getCurrentUser().public_id;
    this.objectInstance.fields = [];
    Object.keys(this.render.fieldsGroups.controls).forEach(field => {
      this.objectInstance.fields.push({
        name: field,
        value: this.render.fieldsGroups.get(field).value
      });
    });
    let ack = null;
    this.objectService.postObject(this.objectInstance).subscribe(newObjectID => {
        ack = newObjectID;
      },
      (error) => {

      }, () => {
        this.router.navigate(['/framework/object/' + ack]);
      });
  }

}
