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

import {Component, OnDestroy, ViewChild} from '@angular/core';
import { CmdbMode } from '../../modes.enum';
import { ObjectBulkChangeEditorComponent } from './object-bulk-change-editor/object-bulk-change-editor.component';
import { ObjectBulkChangePreviewComponent } from './object-bulk-change-preview/object-bulk-change-preview.component';
import { CmdbObject } from '../../models/cmdb-object';
import { FormGroup } from '@angular/forms';
import { ObjectService} from '../../services/object.service';
import { TypeService } from '../../services/type.service';
import { ActivatedRoute, Router } from '@angular/router';
import { httpObserveOptions } from '../../../services/api-call.service';
import { CollectionParameters } from '../../../services/models/api-parameter';
import { takeUntil} from 'rxjs/operators';
import { HttpResponse } from '@angular/common/http';
import { APIGetMultiResponse } from '../../../services/models/api-response';
import { RenderResult } from '../../models/cmdb-render';
import { ReplaySubject } from 'rxjs';

@Component({
  selector: 'cmdb-object-bulk-change',
  templateUrl: './object-bulk-change.component.html',
  styleUrls: ['./object-bulk-change.component.scss']
})
export class ObjectBulkChangeComponent implements OnDestroy {

  @ViewChild(ObjectBulkChangeEditorComponent, {static: true})
  public basicStep: ObjectBulkChangeEditorComponent;

  @ViewChild(ObjectBulkChangePreviewComponent, {static: true})
  public previewStep: ObjectBulkChangePreviewComponent;

  // Subscribe
  private unsubscribe: ReplaySubject<void> = new ReplaySubject<void>();

  public renderResult: RenderResult = undefined;
  public mode: CmdbMode = CmdbMode.Bulk;
  public objectInstance: CmdbObject;
  public activeState: boolean = true;
  public renderForm: FormGroup;
  public fieldsGroups: FormGroup;
  private objectIDs: string[];

  constructor(private objectService: ObjectService, private typeService: TypeService,
              private activeRoute: ActivatedRoute, private route: Router) {
    this.activeRoute.params.subscribe((params) => {
      if (params.typeID !== undefined) {
        const collectionsParams: CollectionParameters = {
          filter: [{ $match: {type_id: Number(params.typeID)}}] , limit: 1,
          sort: 'public_id', order: 1, page: 1
        };
        this.objectService.getObjects(collectionsParams).pipe(takeUntil(this.unsubscribe))
          .subscribe((apiResponse: HttpResponse<APIGetMultiResponse<RenderResult>>) => {
            if (apiResponse.body.results.length > 0) {
              this.renderResult = apiResponse.body.results[0];
            }
            this.objectIDs = params.ids.split(',');
          });
      }
      this.fieldsGroups = new FormGroup({
      });
      this.renderForm = new FormGroup({
      });
    });
  }

  public toggleChange() {
    this.activeState = this.activeState !== true;
    this.renderForm.get('changedFields').value.set('activeObj-isChanged', this.activeState);
  }

  public saveObject() {
    if (this.renderForm.get('changedFields').value.size > 0 ) {
      const httpOptions = Object.assign({}, httpObserveOptions);
      httpOptions.params = {objectIDs: this.objectIDs};

      const patchValue = [];
      const newObjectInstance = new CmdbObject();
      newObjectInstance.active = this.activeState;
      newObjectInstance.type_id = this.renderResult.type_information.type_id;
      newObjectInstance.fields = [];
      this.renderForm.get('changedFields').value.delete('activeObj-isChanged');
      Object.keys(this.renderForm.value).forEach((key: string) => {
        if (key.match('-isChanged') == null
        && this.renderForm.get('changedFields').value.has(key)) {
          patchValue.push({
            name: key,
            value: this.renderForm.value[key] === undefined ? '' : this.renderForm.value[key]
          });
        }
      });
      newObjectInstance.fields = patchValue;
      this.objectService.putObject(0, newObjectInstance, httpOptions).pipe(takeUntil(this.unsubscribe))
        .subscribe((res: boolean) => {
        if (res) {
          this.route.navigate(['/framework/object/type', this.renderResult.type_information.type_id]);
        }
      });
    }
  }

  public ngOnDestroy(): void {
    this.unsubscribe.next();
    this.unsubscribe.complete();
  }
}
