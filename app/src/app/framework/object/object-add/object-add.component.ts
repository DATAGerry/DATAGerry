/*
* DATAGERRY - OpenSource Enterprise CMDB
* Copyright (C) 2024 becon GmbH
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
*
* You should have received a copy of the GNU Affero General Public License
* along with this program. If not, see <https://www.gnu.org/licenses/>.
*/

import { Component, EventEmitter, HostListener, OnDestroy, OnInit, Output, ViewChild } from '@angular/core';
import { TypeService } from '../../services/type.service';
import { CmdbType } from '../../models/cmdb-type';
import { UntypedFormControl, UntypedFormGroup, Validators } from '@angular/forms';
import { BehaviorSubject, Observable, ReplaySubject } from 'rxjs';
import { CmdbMode } from '../../modes.enum';
import { RenderComponent } from '../../render/render.component';
import { CmdbObject } from '../../models/cmdb-object';
import { UserService } from '../../../management/services/user.service';
import { ObjectService } from '../../services/object.service';
import { ActivatedRoute, Router } from '@angular/router';
import { SidebarService } from '../../../layout/services/sidebar.service';
import { AccessControlPermission } from '../../../acl/acl.types';
import { ToastService } from '../../../layout/toast/toast.service';
import { takeUntil } from 'rxjs/operators';
import { LocationService } from '../../services/location.service';
import { APIUpdateMultiResponse } from '../../../services/models/api-response';

@Component({
  selector: 'cmdb-object-add',
  templateUrl: './object-add.component.html',
  styleUrls: ['./object-add.component.scss']
})
export class ObjectAddComponent implements OnInit, OnDestroy {

  public typeList: CmdbType[] = [];
  public typeIDForm: UntypedFormGroup;
  private typeIDSubject: BehaviorSubject<number>;
  public typeID: Observable<number>;
  public typeInstance: CmdbType;
  public mode: CmdbMode = CmdbMode.Create;
  public objectInstance: CmdbObject;
  public renderForm: UntypedFormGroup;
  public fieldsGroups: UntypedFormGroup;

  @Output() parentSubmit = new EventEmitter<any>();
  @ViewChild(RenderComponent, {static: false}) render: RenderComponent;

  /**
   * Global un-subscriber for http calls to the rest backend.
   */
  private subscriber: ReplaySubject<void> = new ReplaySubject<void>();
  private parentID: number;


  /* ------------------------------------------------------------------------------------------------------------------ */
  /*                                                     LIFE CYCLE                                                     */
  /* ------------------------------------------------------------------------------------------------------------------ */

  constructor(private router: Router, 
              private typeService: TypeService, 
              private objectService: ObjectService, 
              private userService: UserService, 
              private route: ActivatedRoute,
              private sidebarService: SidebarService,
              private locationService: LocationService, 
              private toastService: ToastService) {

    this.objectInstance = new CmdbObject();
    this.typeIDSubject = new BehaviorSubject<number>(null);

    this.route.params.subscribe((params) => {
      if (params.publicID !== undefined) {
        this.typeIDSubject.next(+params.publicID);
      }
    });

    this.typeID = this.typeIDSubject.asObservable();

    this.typeID.pipe(takeUntil(this.subscriber)).subscribe(selectedTypeID => {
      if (selectedTypeID !== null) {
        this.typeService.getType(selectedTypeID).subscribe((typeInstance: CmdbType) => {
          this.typeInstance = typeInstance;
        });
      }
    });

    this.fieldsGroups = new UntypedFormGroup({});
    this.renderForm = new UntypedFormGroup({
      active: new UntypedFormControl(true)
    });
  }

  public ngOnInit(): void {
    this.typeService.getTypeList(AccessControlPermission.CREATE).pipe(takeUntil(this.subscriber)).subscribe((typeList: CmdbType[]) => {
      this.typeList = typeList;
    }, 
    (error) => {
      this.toastService.error(error);
    });

    this.typeIDForm = new UntypedFormGroup({
      typeID: new UntypedFormControl(null, Validators.required)
    });

  }


  public ngOnDestroy(): void {
    this.typeIDSubject.unsubscribe();
    this.subscriber.next();
    this.subscriber.complete();
  }


/* ------------------------------------------------------------------------------------------------------------------ */
/*                                                       METHODS                                                      */
/* ------------------------------------------------------------------------------------------------------------------ */

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
              let val = this.renderForm.value[field];

              if(field == 'dg_location'){
                this.parentID = val;
              }

              if (val === undefined || val == null) { val = ''; }
              this.objectInstance.fields.push({
                  name: field,
                  value: val
              });
          });
        
          let newID = null;
          this.objectService.postObject(this.objectInstance).pipe(takeUntil(this.subscriber)).subscribe(newObjectID => {
                newID = newObjectID;
                this.createLocation(newID);
            },
            (e) => {
                console.error(e);
            }, 
            () => {
                this.router.navigate(['/framework/object/view/' + newID]);
                this.sidebarService.updateTypeCounter(this.typeInstance.public_id);
                this.toastService.success(`Object ${ newID } was created succesfully!`);
            });
      }
  }

  private createLocation(newObjectID: number){
    let params = {
      "object_id": newObjectID,
      "parent": this.parentID,
      "name": this.locationService.locationTreeName,
      "type_id": this.objectInstance.type_id 
    }

    if(this.parentID){
      this.locationService.postLocation(params).subscribe((res: APIUpdateMultiResponse) => {
        this.locationService.locationTreeName = "";
      }, error => {
        this.toastService.error(error);
      });
    }

  }

/* ------------------------------------------------------------------------------------------------------------------ */
/*                                                   HELPER SECTION                                                   */
/* ------------------------------------------------------------------------------------------------------------------ */
    @HostListener('window:scroll')
    onWindowScroll() {
        const dialog = document.getElementById('object-form-action');

        if (dialog) {
            if ((document.body.scrollTop > 10 || document.documentElement.scrollTop > 10)) {
                dialog.style.visibility = 'visible';
            } else {
                dialog.style.visibility = 'hidden';
            }
        }
    }

}
