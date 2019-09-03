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

import { Component, OnInit } from '@angular/core';
import { ApiCallService } from '../../../services/api-call.service';
import { ObjectService } from '../../services/object.service';
import { TypeService } from '../../services/type.service';
import { ActivatedRoute, Router } from '@angular/router';
import { CmdbMode } from '../../modes.enum';
import { CmdbObject } from '../../models/cmdb-object';
import { CmdbType } from '../../models/cmdb-type';
import { FormControl, FormGroup } from '@angular/forms';
import { ToastService } from '../../../layout/services/toast.service';
import { RenderResult } from '../../models/cmdb-render';
import { RenderService } from '../../render/service/render.service';

@Component({
  selector: 'cmdb-object-edit',
  templateUrl: './object-edit.component.html',
  styleUrls: ['./object-edit.component.scss']
})
export class ObjectEditComponent implements OnInit {

  public mode: CmdbMode = CmdbMode.Edit;
  private objectID: number;
  public renderResult: RenderResult;
  public objectInstance: CmdbObject;
  public renderForm: FormGroup;
  public commitForm: FormGroup;

  constructor(private api: ApiCallService, private renderService: RenderService, private objectService: ObjectService,
              private route: ActivatedRoute, private router: Router, private toastService: ToastService) {
    this.route.params.subscribe((params) => {
      this.objectID = params.publicID;
    });
    this.renderForm = new FormGroup({});
    this.commitForm = new FormGroup({
      comment: new FormControl('')
    });
  }

  public ngOnInit(): void {
    this.renderService.getRenderResult(this.objectID).subscribe((rr: RenderResult) => {
      this.renderResult = rr;
    }, (error) => {
      console.error(error);
    }, () => {
      this.objectService.getObject(this.objectID, true).subscribe(ob => {
        this.objectInstance = ob;
      });
    });
  }

  public editObject(): void {
    this.renderForm.markAllAsTouched();
    if (this.renderForm.valid) {
      const patchValue = [];

      Object.keys(this.renderForm.value).forEach((key: string) => {
        patchValue.push({
          name: key,
          value: this.renderForm.value[key]
        });
      });

      this.objectInstance.fields = patchValue;
      this.objectInstance.comment = this.commitForm.get('comment').value;
      this.objectService.putObject(this.objectID, this.objectInstance).subscribe((res: boolean) => {
        if (res) {
          this.toastService.show('Object was updated!');
          this.router.navigate(['/framework/object/view/' + this.objectID]);
        }
      });
    }
  }

}
