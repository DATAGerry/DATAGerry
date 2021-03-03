/*
* DATAGERRY - OpenSource Enterprise CMDB
* Copyright (C) 2019 - 2021 NETHINKS GmbH
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
* along with this program. If not, see <https://www.gnu.org/licenses/>.
*/

import { Component, Input, OnDestroy, OnInit } from '@angular/core';
import { TypeService } from '../../../../services/type.service';
import { ConfigEditBaseComponent } from '../config.edit';
import { RenderResult } from '../../../../models/cmdb-render';
import { ObjectService } from '../../../../services/object.service';
import { CmdbType } from '../../../../models/cmdb-type';
import { CollectionParameters } from '../../../../../services/models/api-parameter';
import { takeUntil } from 'rxjs/operators';
import { APIGetMultiResponse } from '../../../../../services/models/api-response';
import { Sort, SortDirection } from '../../../../../layout/table/table.types';
import { ReplaySubject } from 'rxjs';
import { ToastService } from '../../../../../layout/toast/toast.service';

@Component({
  selector: 'cmdb-ref-field-edit',
  templateUrl: './ref-field-edit.component.html',
  styleUrls: ['./ref-field-edit.component.scss'],
})
export class RefFieldEditComponent extends ConfigEditBaseComponent implements OnInit, OnDestroy {

  constructor(private typeService: TypeService, private objectService: ObjectService, private toast: ToastService) {
    super();
  }
  @Input() groupList: any;
  @Input() userList: any;

  /**
   * Global un-subscriber for http calls to the rest backend.
   */
  private subscriber: ReplaySubject<void> = new ReplaySubject<void>();

  /**
   * Type list for reference selection
   */
  public typesAPIResponse: APIGetMultiResponse<CmdbType>;
  public typeList: Array<CmdbType>;
  public filteredTypeList: CmdbType[] = [];
  public totalTypes: number = 0;

  /**
   * Total number of Types pages.
   */
  public totalTypesPages: number = 0;

  /**
   * loading indicator?
   */
  public typeLoading: boolean = false;

  /**
   * Begin with first page.
   */
  public readonly initPage: number = 1;
  public page: number = this.initPage;

  /**
   * Filter query from the table search input.
   */
  public filter: string;

  /**
   * Default sort filter.
   */
  public sort: Sort = { name: 'public_id', order: SortDirection.DESCENDING } as Sort;

  /**
   * Nested summaries
   */
  public summaries: any[] = [];

  /**
   * Object list for default reference value
   */
  public objectList: RenderResult[] = [];
  public filteredObjectList: RenderResult[] = [];

  /**
   * Types params
   */
  public typesParams: CollectionParameters = {
    filter: undefined, limit: 0, sort: 'public_id', order: 1, page: 1
  };

  public ngOnInit(): void {
    this.typeLoading = true;
    this.typeService.getTypes(this.typesParams).pipe(takeUntil(this.subscriber)).subscribe(
      (apiResponse: APIGetMultiResponse<CmdbType>) => {
        this.typeList = apiResponse.results as Array<CmdbType>;
        this.totalTypes = apiResponse.total;
        this.prepareSummaries();
        this.typeLoading = false;
      },
      (err) => this.toast.error(err)).add(() => this.typeLoading = false);

    if (this.data.value !== null && this.data.value !== undefined && this.data.value !== '') {
      this.objectService.getObjectsByType(this.data.ref_types).subscribe((res: RenderResult[]) => {
        this.objectList = res;
      });
    }
  }

  /**
   * Structure of the Summaries depending on the selected types
   * @private
   */
  private prepareSummaries() {
    if (this.data.ref_types) {
      if (!Array.isArray(this.data.ref_types)) {
        this.data.ref_types = [this.data.ref_types];
      }
      this.filteredTypeList = this.typeList.filter(type => this.data.ref_types.includes(type.public_id));
      this.data.summaries = this.data.summaries ? this.data.summaries : this.summaries;
      this.summaries = this.data.summaries;
    }
  }

  public onChange() {
    const {ref_types} = this.data;
    if (ref_types && ref_types.length === 0) {
      this.objectList = [];
      this.filteredTypeList = [];
      this.data.value = '';
    } else {
      this.objectService.getObjectsByType(ref_types).subscribe((res: RenderResult[]) => {
        this.objectList = res;
        this.prepareSummaries();
      });
    }
  }

  public summaryFieldFilter(id: number) {
    return id ? this.typeList.find(s => s.public_id === id).fields : [];
  }

  public changeSummaryOption(type: CmdbType) {
    const nestedSummary = this.summaries.find(s => s.type_id === type.public_id);
    nestedSummary.label = type.label;
    nestedSummary.icon = type.render_meta.icon;
  }

  public changeDefault(value: any) {
    this.data.default = parseInt(value, 10);
    return this.data.default;
  }

  public addSummary() {
    if (this.filteredTypeList) {
      this.summaries.push({
        type_id: null,
        line: null,
        label: null,
        fields: [],
        icon: null,
        prefix: false,
      });
    }
  }

  public delSummary(value: any) {
    if (this.summaries.length > 0) {
      const index = this.summaries.indexOf(value, 0);
      if (index > -1) {
        this.summaries.splice(index, 1);
      }
    }
  }

  /**
   * Destroy subscriptions after closed.
   */
  public ngOnDestroy(): void {
    this.subscriber.next();
    this.subscriber.complete();
  }

}
