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

import {Component, EventEmitter, HostListener, OnDestroy, OnInit, Output, ViewChild} from '@angular/core';
import { TypeService } from '../../services/type.service';
import { CmdbType } from '../../models/cmdb-type';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { BehaviorSubject, Observable } from 'rxjs';
import { CmdbMode } from '../../modes.enum';
import { RenderComponent } from '../../render/render.component';
import { CmdbObject } from '../../models/cmdb-object';
import { UserService } from '../../../management/services/user.service';
import { ObjectService } from '../../services/object.service';
import { ActivatedRoute, Router } from '@angular/router';
import { CategoryService } from '../../services/category.service';
import { error } from 'selenium-webdriver';
import { CmdbCategory } from '../../models/cmdb-category';

@Component({
  selector: 'cmdb-object-add',
  templateUrl: './object-add.component.html',
  styleUrls: ['./object-add.component.scss']
})
export class ObjectAddComponent implements OnInit, OnDestroy {

  public typeList: CmdbType[];
  public preperatedTypeList: any[];
  public typeIDForm: FormGroup;
  private typeIDSubject: BehaviorSubject<number>;
  public typeID: Observable<number>;
  public typeInstance: CmdbType;
  public mode: CmdbMode = CmdbMode.Create;
  public objectInstance: CmdbObject;
  public renderForm: FormGroup;
  public fieldsGroups: FormGroup;
  @Output() parentSubmit = new EventEmitter<any>();
  @ViewChild(RenderComponent, {static: false}) render: RenderComponent;


  constructor(private router: Router, private typeService: TypeService, private categoryService: CategoryService,
              private objectService: ObjectService, private userService: UserService, private route: ActivatedRoute) {

    this.objectInstance = new CmdbObject();
    this.typeIDSubject = new BehaviorSubject<number>(null);
    this.route.params.subscribe((params) => {
      if (params.publicID !== undefined) {
        this.typeIDSubject.next(+params.publicID);
      }
    });
    this.typeID = this.typeIDSubject.asObservable();
    this.typeID.subscribe(selectedTypeID => {
      if (selectedTypeID !== null) {
        this.typeService.getType(selectedTypeID).subscribe((typeInstance: CmdbType) => {
          this.typeInstance = typeInstance;
        });
      }
    });
    this.fieldsGroups = new FormGroup({});
    this.renderForm = new FormGroup({
      active: new FormControl(true)
    });
  }

  public ngOnInit(): void {
    this.typeService.getTypeList().subscribe((typeList: CmdbType[]) => {
      this.typeList = typeList;
      this.preperatedTypeList = [];
    }, (e) => {
      console.error(e);
    }, () => {
      this.categoryService.getCategoryList().subscribe((categoryList: CmdbCategory[]) => {
        categoryList.forEach( category => {
          for ( const type of this.typeList ) {
            if ((type.category_id === category.public_id)
              || (category.root && type.category_id === 0) ) {
              type.category_name = category.label;
              this.preperatedTypeList.push(type);
            }
          }
        });
      }, (e) => {
        console.log(e);
      }, () => {
        this.typeList = this.preperatedTypeList;
      });
    });
    this.typeIDForm = new FormGroup({
      typeID: new FormControl(null, Validators.required)
    });

  }

  @HostListener('window:scroll', ['$event'])
  onWindowScroll($event) {
    const dialog = document.getElementById('object-form-action');
    if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
      dialog.style.display = 'block';
    } else {
      dialog.style.display = 'none';
    }
  }

  public ngOnDestroy(): void {
    this.typeIDSubject.unsubscribe();
  }

  groupByFn = (item) => item.category_name;

  groupValueFn = (_: string, children: any[]) => ({name: children[0].category_name, total: children.length});


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
    this.renderForm.markAllAsTouched();
    if (this.renderForm.valid) {
      this.objectInstance.type_id = this.currentTypeID;
      this.objectInstance.version = '1.0.0';
      this.objectInstance.author_id = this.userService.getCurrentUser().public_id;
      this.objectInstance.fields = [];
      this.render.renderForm.removeControl('active');
      Object.keys(this.render.renderForm.controls).forEach(field => {
        this.objectInstance.fields.push({
          name: field,
          value: this.render.renderForm.get(field).value || ''
        });
      });
      let ack = null;
      this.objectService.postObject(this.objectInstance).subscribe(newObjectID => {
          ack = newObjectID;
        },
        (e) => {
          console.error(e);
        }, () => {
          this.router.navigate(['/framework/object/view/' + ack]);
        });
    }
  }

}
