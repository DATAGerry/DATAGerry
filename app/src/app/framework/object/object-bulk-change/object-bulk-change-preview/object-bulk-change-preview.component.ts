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

import { Component, Input, OnInit, ViewChild } from '@angular/core';
import { ObjectService } from '../../../services/object.service';
import { DataTableFilter, DataTablesResult } from '../../../models/cmdb-datatable';
import { ActivatedRoute } from '@angular/router';
import { FormGroup } from '@angular/forms';
import { JwPaginationComponent } from 'jw-angular-pagination';
import { CmdbMode } from '../../../modes.enum';

@Component({
  selector: 'cmdb-object-bulk-change-preview',
  templateUrl: './object-bulk-change-preview.component.html',
  styleUrls: ['./object-bulk-change-preview.component.scss']
})
export class ObjectBulkChangePreviewComponent implements OnInit {

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

  private typeID: number;
  public SIMPLEMODE: CmdbMode = CmdbMode.Simple;
  public renderResult: DataTablesResult;
  public readonly limit: number = 10;
  public currentPage: number = 1;
  public maxNumberOfSites: number[];
  public dtFilter: DataTableFilter = new DataTableFilter();

  constructor(private objectService: ObjectService, private activeRoute: ActivatedRoute) {
    this.activeRoute.params.subscribe((params) => {
      if (params.ids !== undefined) {
        this.dtFilter.start = 0;
        this.dtFilter.length = 10;
        this.dtFilter.search = '';
        this.dtFilter.dtRender = false;
        this.dtFilter.idList = params.ids.split(',');
      }
      if (params.typeID !== undefined) {
        this.typeID = params.typeID;
      }
    });
  }

  ngOnInit(): void {
    this.loadData();
  }

  private loadData() {
    this.objectService.getObjectsByFilter(this.typeID, this.dtFilter).subscribe(value => {
      this.renderResult = value;
      if (this.dtFilter.start === 0) {
        this.maxNumberOfSites = Array.from({ length: (this.renderResult.recordsTotal) }, (v, k) => k + 1);
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

  public onChangePage(event): void {
    if (this.currentPage !== this.pagination.pager.currentPage) {
      this.currentPage = this.pagination.pager.currentPage;
      this.dtFilter.start = (this.currentPage - 1) * this.limit;
      this.loadData();
    }
  }
}
