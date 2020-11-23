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

import { Component, EventEmitter, Input, Output, ViewChild } from '@angular/core';
import { FormGroup } from '@angular/forms';
import { JwPaginationComponent } from 'jw-angular-pagination';
import { CmdbMode } from '../../../modes.enum';
import { CollectionParameters } from '../../../../services/models/api-parameter';
import { RenderResult } from '../../../models/cmdb-render';

@Component({
  selector: 'cmdb-object-bulk-change-preview',
  templateUrl: './object-bulk-change-preview.component.html',
  styleUrls: ['./object-bulk-change-preview.component.scss']
})
export class ObjectBulkChangePreviewComponent {

  @ViewChild('paginationBulkChanges', { static: false }) pagination: JwPaginationComponent;

  @Output() reloadData = new EventEmitter<any>();

  // Data Binding
  @Input() renderForm: FormGroup;
  @Input() selectedObjectIds: number[];
  @Input() currentPage: number;
  @Input() maxNumberOfSites: number[];

  private objectState: boolean;
  @Input()
  public set activeState(value: boolean) {
    this.objectState = value;
  }

  public get activeState(): boolean {
    return this.objectState;
  }

  private result: Array<RenderResult> = [];
  @Input()
  public set renderResult(value: Array<RenderResult>) {
    this.result = value;
  }

  public get renderResult(): Array<RenderResult> {
    return this.result;
  }

  // Render-Page-View information
  public readonly mode: CmdbMode = CmdbMode.Simple;

  constructor() {
  }

  public loadData(): void {
    const params: CollectionParameters = {
      filter: [{ $match:
          {
            $and: [
              {type_id: this.renderResult[0].type_information.type_id},
              { public_id: { $in: this.selectedObjectIds }}]
          }
      }] , limit: 10,
      sort: 'public_id', order: 1, page: this.currentPage
    };
    this.reloadData.emit(params);
  }

  public activeStateChanged(): boolean {
    return this.renderForm.get('changedFields').value.get('activeObj-isChanged');
  }

  public mergeFields(fields: any) {
    return fields.filter(field => this.renderForm.get('changedFields').value.get(field.name));
  }

  public changes(field: any) {
    const temp = this.renderForm.get('changedFields').value.get(field.name);
    temp.value = this.renderForm.get(field.name).value;
    if (temp.hasOwnProperty('reference')) {
      temp.reference = {
        summaries: [],
        type_label: '',
        icon: ''
      };
    }
    return temp;
  }

  public onChangePage(): void {
    if (this.currentPage !== this.pagination.pager.currentPage) {
      this.currentPage = this.pagination.pager.currentPage;
      this.loadData();
    }
  }
}
