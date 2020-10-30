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
* along with this program. If not, see <https://www.gnu.org/licenses/>.
*/

import {
  AfterViewInit,
  Component, ComponentFactoryResolver, ElementRef, Injector,
  OnDestroy,
  OnInit, TemplateRef, ViewChild,
} from '@angular/core';
import { BehaviorSubject, ReplaySubject, Subject } from 'rxjs';
import { CmdbType } from '../../models/cmdb-type';
import { ActivatedRoute, Data, Router } from '@angular/router';
import { takeUntil } from 'rxjs/operators';
import { RenderResult } from '../../models/cmdb-render';
import { TableComponent } from '../../../layout/table/table.component';
import { Column, Sort, SortDirection } from '../../../layout/table/table.types';
import { ObjectService } from '../../services/object.service';
import { CollectionParameters } from '../../../services/models/api-parameter';
import { HttpResponse } from '@angular/common/http';
import { APIGetMultiResponse } from '../../../services/models/api-response';
import { UserCompactComponent } from '../../../management/users/components/user-compact/user-compact.component';
import { ActiveBadgeComponent } from '../../../layout/helpers/active-badge/active-badge.component';
import { ObjectTableActionsComponent } from '../components/object-table-actions/object-table-actions.component';
import { FormGroup } from '@angular/forms';
import { CmdbMode } from '../../modes.enum';

@Component({
  selector: 'cmdb-objects-by-type',
  templateUrl: './objects-by-type.component.html',
  styleUrls: ['./objects-by-type.component.scss']
})
export class ObjectsByTypeComponent implements OnInit, OnDestroy {

  /**
   * Table component.
   */
  @ViewChild(TableComponent, { static: false }) objectsTableComponent: TableComponent<RenderResult>;

  @ViewChild('activeTemplate', { static: true }) activeTemplate: TemplateRef<any>;
  @ViewChild('fieldTemplate', { static: true }) fieldTemplate: TemplateRef<any>;
  @ViewChild('actionTemplate', { static: true }) actionTemplate: TemplateRef<any>;

  /**
   * Component un-subscriber.
   */
  private subscriber: ReplaySubject<void> = new ReplaySubject<void>();

  /**
   * Current render results
   */
  public results: Array<RenderResult> = [];

  /**
   * Total number of results
   */
  public totalResults: number = 0;

  /**
   * Current type from the route resolve.
   */
  private typeSubject: BehaviorSubject<CmdbType> = new BehaviorSubject<CmdbType>(undefined);

  public mode: CmdbMode = CmdbMode.Simple;
  public renderForm: FormGroup;

  public sort: Sort = { name: 'public_id', order: SortDirection.DESCENDING } as Sort;

  public get type(): CmdbType {
    return this.typeSubject.getValue() as CmdbType;
  }

  public columns: Array<Column>;

  public page: number = 1;
  public limit: number = 10;

  constructor(private router: Router, private route: ActivatedRoute, private objectService: ObjectService) {
    this.route.data.pipe(takeUntil(this.subscriber)).subscribe((data: Data) => {
      this.typeSubject.next(data.type as CmdbType);
    });
  }

  public ngOnInit(): void {
    this.typeSubject.asObservable().pipe(takeUntil(this.subscriber)).subscribe((type: CmdbType) => {
      this.setColumns(type);
      this.getObjects();
    });
  }

  private setColumns(type: CmdbType): void {

    const fields = type.fields || [];
    const summaryFields = type.render_meta.summary.fields || [];

    const columns = [
      {
        display: 'Active',
        name: 'active',
        data: 'active',
        sortable: false,
        searchable: false,
        template: this.activeTemplate,
        cssClasses: ['text-center']
      },
      {
        display: 'Public ID',
        name: 'public_id',
        data: 'object_information.object_id',
        searchable: false,
        sortable: true
      },

    ] as Array<Column>;

    for (const field of fields) {
      columns.push({
        display: field.label || field.name,
        name: field.name,
        sortable: true,
        searchable: true,
        hidden: !summaryFields.includes(field.name),
        template: this.fieldTemplate
      } as Column);
    }

    columns.push({
      display: 'Actions',
      name: 'actions',
      sortable: false,
      searchable: false,
      fixed: true,
      template: this.actionTemplate,
      cssClasses: ['text-center']
    } as Column);

    this.columns = columns;
  }

  public getFieldByName(item: RenderResult, name: string) {
    return item.fields.find(field => field.name === name);
  }

  public getFieldValue(item: RenderResult, name: string) {
    const value = item.fields.find(field => field.name === name).value;
    if (value) {
      return value;
    } else {
      return {};
    }
  }

  public getObjects() {
    const params: CollectionParameters = {
      filter: { type_id: this.type.public_id }, limit: this.limit,
      sort: this.sort.name, order: this.sort.order, page: this.page
    };
    this.objectService.getObjects(params).pipe(takeUntil(this.subscriber))
      .subscribe((apiResponse: HttpResponse<APIGetMultiResponse<RenderResult>>) => {
        this.results = apiResponse.body.results as Array<RenderResult>;
        this.totalResults = apiResponse.body.total;
      });
  }


  public ngOnDestroy(): void {
    this.subscriber.next();
    this.subscriber.complete();
  }

  public onPageChange(page: number) {
    this.page = page;
    this.getObjects();
  }

  public onPageSizeChange(limit: number): void {
    this.limit = limit;
    this.getObjects();
  }

  public onSortChange(sort: Sort): void {
    this.sort = sort;
    this.getObjects();
  }


}
