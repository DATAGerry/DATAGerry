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

import {Component, Input, OnDestroy, OnInit, ViewChild} from '@angular/core';
import { ObjectService } from '../../../services/object.service';
import { ActivatedRoute } from '@angular/router';
import { FormGroup } from '@angular/forms';
import { JwPaginationComponent } from 'jw-angular-pagination';
import { CmdbMode } from '../../../modes.enum';
import { CollectionParameters } from '../../../../services/models/api-parameter';
import { takeUntil } from 'rxjs/operators';
import { HttpResponse } from '@angular/common/http';
import { APIGetMultiResponse } from '../../../../services/models/api-response';
import { RenderResult } from '../../../models/cmdb-render';
import { ReplaySubject } from 'rxjs';

@Component({
  selector: 'cmdb-object-bulk-change-preview',
  templateUrl: './object-bulk-change-preview.component.html',
  styleUrls: ['./object-bulk-change-preview.component.scss']
})
export class ObjectBulkChangePreviewComponent implements OnInit, OnDestroy {

  @ViewChild('paginationBulkChanges', { static: false }) pagination: JwPaginationComponent;
  @Input()  renderForm: FormGroup;

  private objectState: boolean;
  @Input()
  set activeState(value: boolean) {
    this.objectState = value;
  }

  get activeState(): boolean {
    return this.objectState;
  }

  // Unsubscribes
  private unsubscribe: ReplaySubject<void> = new ReplaySubject<void>();

  // Render-Page-View information
  private typeID: number;
  public readonly mode: CmdbMode = CmdbMode.Simple;
  public renderResult: Array<RenderResult> = [];
  public selectedBulkObjects: number[] = [];

  // Pagination
  public readonly limit: number = 10;
  public initData: boolean = true;
  public currentPage: number = 1;
  public maxNumberOfSites: number[];

  constructor(private objectService: ObjectService, private activeRoute: ActivatedRoute) {
    this.activeRoute.params.subscribe((params) => {
      if (params.ids !== undefined) {
        this.selectedBulkObjects = Array.from(params.ids.split(','), Number);
      }
      if (params.typeID !== undefined) {
        this.typeID = Number(params.typeID);
      }
    });
  }

  ngOnInit(): void {
    this.loadData();
  }

  private loadData() {
    const params: CollectionParameters = {
      filter: [{ $match:
          {
            $and: [{type_id: this.typeID} , { public_id: { $in: this.selectedBulkObjects }}]
          }
      }] , limit: 10,
      sort: 'public_id', order: 1, page: this.currentPage
    };
    this.objectService.getObjects(params).pipe(takeUntil(this.unsubscribe))
      .subscribe((apiResponse: HttpResponse<APIGetMultiResponse<RenderResult>>) => {
        this.renderResult = apiResponse.body.results;
        if (this.initData) {
          this.maxNumberOfSites = Array.from({ length: (apiResponse.body.total) }, (v, k) => k + 1);
          this.initData = false;
        }
      });
  }

  public mergeFields(fields: any) {
    return fields.filter(field => this.renderForm.get('changedFields').value.get(field.name));
  }

  public activeStateChanged(): boolean {
    return this.renderForm.get('changedFields').value.get('activeObj-isChanged');
  }

  public changes(field: any) {
    const temp = this.renderForm.get('changedFields').value.get(field.name);
    temp.value = this.renderForm.get(temp.name).value;
    return temp;
  }

  public onChangePage(): void {
    if (this.currentPage !== this.pagination.pager.currentPage) {
      this.currentPage = this.pagination.pager.currentPage;
      this.loadData();
    }
  }

  ngOnDestroy(): void {
    this.unsubscribe.next();
    this.unsubscribe.complete();
  }
}
