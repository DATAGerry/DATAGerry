/*
* DATAGERRY - OpenSource Enterprise CMDB
* Copyright (C) 2023 becon GmbH
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

import { Component, HostListener, OnInit } from '@angular/core';
import { ApiCallService } from '../../../services/api-call.service';
import { ObjectService } from '../../services/object.service';
import { ActivatedRoute, Router } from '@angular/router';
import { CmdbMode } from '../../modes.enum';
import { CmdbObject } from '../../models/cmdb-object';
import { UntypedFormControl, UntypedFormGroup } from '@angular/forms';
import { ToastService } from '../../../layout/toast/toast.service';
import { RenderResult } from '../../models/cmdb-render';
import { TypeService } from '../../services/type.service';
import { CmdbType } from '../../models/cmdb-type';
import { APIUpdateMultiResponse } from '../../../services/models/api-response';
import {text} from "@fortawesome/fontawesome-svg-core";
import { SidebarService } from 'src/app/layout/services/sidebar.service';

@Component({
  selector: 'cmdb-object-edit',
  templateUrl: './object-edit.component.html',
  styleUrls: ['./object-edit.component.scss']
})
export class ObjectEditComponent implements OnInit {

  public mode: CmdbMode = CmdbMode.Edit;
  public objectInstance: CmdbObject;
  public typeInstance: CmdbType;
  public renderResult: RenderResult;
  public renderForm: UntypedFormGroup;
  public commitForm: UntypedFormGroup;
  private objectID: number;
  public activeState : boolean ;

  constructor(private api: ApiCallService, private objectService: ObjectService, private typeService: TypeService,
              private route: ActivatedRoute, private router: Router, private toastService: ToastService , 
              private sidebarService : SidebarService) {
    this.route.params.subscribe((params) => {
      this.objectID = params.publicID;
    });
    this.renderForm = new UntypedFormGroup({});
    this.commitForm = new UntypedFormGroup({
      comment: new UntypedFormControl('')
    });
  }

  public ngOnInit(): void {
    this.objectService.getObject(this.objectID).subscribe((rr: RenderResult) => {
        this.renderResult = rr;
        this.activeState = this.renderResult.object_information.active;
      },
      error => {
        console.error(error);
      },
      () => {
        this.objectService.getObject<CmdbObject>(this.objectID, true).subscribe(ob => {
          this.objectInstance = ob;
        });
        this.typeService.getType(this.renderResult.type_information.type_id).subscribe((value: CmdbType) => {
          this.typeInstance = value;
        });
      });
  }

  @HostListener('window:scroll', ['$event'])
  onWindowScroll($event) {
    const dialog = document.getElementById('object-form-action');
    if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
      dialog.style.visibility = 'visible';
    } else {
      dialog.style.visibility = 'hidden';
    }
  }

  public editObject(): void {
    this.renderForm.markAllAsTouched();
    if (this.renderForm.valid) {
      const patchValue = [];

      Object.keys(this.renderForm.value).forEach((key: string) => {
        let val = this.renderForm.value[key];
        if (val === undefined || val == null) { val = ''; }
        patchValue.push({
          name: key,
          value: val
        });
      });

      this.objectInstance.fields = patchValue;
      this.objectInstance.comment = this.commitForm.get('comment').value;
      this.objectInstance.active = this.activeState;
      this.objectService.putObject(this.objectID, this.objectInstance).subscribe((res: APIUpdateMultiResponse) => {
        if (res.failed.length === 0) {
          this.objectService.changeState(this.objectID, this.activeState).subscribe((resp: boolean) => {
            this.sidebarService.ReloadSideBarData();
          });
          this.toastService.success('Object was successfully updated!');
          this.router.navigate(['/framework/object/view/' + this.objectID]);
        } else {
          for (const err of res.failed) {
            this.toastService.error(err.error_message);
          }
          this.router.navigate(['/framework/object/type/' + this.objectInstance.type_id]);
        }
      }, error => {
        this.toastService.error(error);
        this.router.navigate(['/framework/object/type/' + this.objectInstance.type_id]);
      });
    }
  }

  public toggleChange() {
    this.activeState = this.activeState !== true;
    this.renderForm.markAsDirty();
    }

}
