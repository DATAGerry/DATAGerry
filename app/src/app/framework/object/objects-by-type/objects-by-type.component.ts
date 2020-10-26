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
import { ReplaySubject } from 'rxjs';
import { CmdbType } from '../../models/cmdb-type';
import { ActivatedRoute, Data, Router } from '@angular/router';
import { takeUntil } from 'rxjs/operators';
import { RenderResult } from '../../models/cmdb-render';
import { TableComponent } from '../../../layout/table/table.component';
import { Column } from '../../../layout/table/models';
import { ObjectService } from '../../services/object.service';
import { CollectionParameters } from '../../../services/models/api-parameter';
import { HttpResponse } from '@angular/common/http';
import { APIGetMultiResponse } from '../../../services/models/api-response';
import { UserCompactComponent } from '../../../management/users/components/user-compact/user-compact.component';

@Component({
  selector: 'cmdb-objects-by-type',
  templateUrl: './objects-by-type.component.html',
  styleUrls: ['./objects-by-type.component.scss']
})
export class ObjectsByTypeComponent implements OnInit, AfterViewInit, OnDestroy {

  /**
   * Table component.
   */
  @ViewChild(TableComponent, { static: false }) objectsTableComponent: TableComponent<RenderResult>;

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
  public type: CmdbType;

  /**
   * Preset list of columns.
   */
  public readonly defaultPreColumns: Array<Column> = [
    {
      name: 'Active',
      data: 'active',
      sortable: true
    },
    {
      name: 'Public ID',
      data: 'object_information.object_id',
      sortable: true
    }
  ] as Array<Column>;

  public readonly defaultAppendColumns: Array<Column> = [
    {
      name: 'Author',
      data: 'object_information.author_id',
      display: 'object_information.author_name',
      sortable: true,
    },
    {
      name: 'Actions',
      sortable: false,
      fixed: true,
      render(item?: any, column?: Column, index?: number) {
        return 'Test';
      }
    }
  ] as Array<Column>;

  public columns: Array<Column>;


  constructor(private router: Router, private route: ActivatedRoute, private objectService: ObjectService) {
  }

  public ngOnInit() {
    // Subscribe to route changes
    this.route.data.pipe(takeUntil(this.subscriber)).subscribe((data: Data) => {
      this.type = data.type as CmdbType;
    });
    const typeColumns: Array<Column> = [] as Array<Column>;
    this.columns = [...this.defaultPreColumns, ...typeColumns, ...this.defaultAppendColumns];
  }

  public ngAfterViewInit(): void {
    const params: CollectionParameters = {
      filter: { type_id: this.type.public_id }, limit: 10,
      sort: 'public_id', order: 1, page: 1
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


}
