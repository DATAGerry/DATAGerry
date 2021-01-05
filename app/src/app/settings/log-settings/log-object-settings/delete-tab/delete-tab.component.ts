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

import { Component, EventEmitter, Input, OnDestroy, OnInit, Output, TemplateRef, ViewChild } from '@angular/core';
import { CmdbLog } from '../../../../framework/models/cmdb-log';
import { Column, Sort, SortDirection } from '../../../../layout/table/table.types';
import { CollectionParameters } from '../../../../services/models/api-parameter';
import { LogService } from '../../../../framework/services/log.service';
import { APIGetMultiResponse } from '../../../../services/models/api-response';
import { DatePipe } from '@angular/common';
import { TableComponent } from '../../../../layout/table/table.component';
import { ReplaySubject } from 'rxjs';
import { takeUntil } from 'rxjs/operators';

@Component({
  selector: 'cmdb-delete-tab',
  templateUrl: './delete-tab.component.html',
  styleUrls: ['./delete-tab.component.scss']
})
export class DeleteTabComponent implements OnInit, OnDestroy {

  @Output() deleteEmitter = new EventEmitter<number>();
  @Output() cleanUpEmitter = new EventEmitter<number[]>();

  /**
   * Component un-subscriber.
   */
  private subscriber: ReplaySubject<void> = new ReplaySubject<void>();

  /**
   * Table component.
   */
  @ViewChild(TableComponent, { static: false }) objectsTableComponent: TableComponent<CmdbLog>;

  @ViewChild('dateTemplate', {static: true}) dateTemplate: TemplateRef<any>;

  @ViewChild('dataTemplate', {static: true}) dataTemplate: TemplateRef<any>;

  @ViewChild('changeTemplate', {static: true}) changeTemplate: TemplateRef<any>;

  @ViewChild('userTemplate', {static: true}) userTemplate: TemplateRef<any>;

  @Input() set reloadLogs(value: boolean) {
    if (value) {
      this.resetCollectionParameters();
      this.loadDeleted();
    }
  }

  public selectedLogIDs: Array<number> = [];

  public filter: string;

  public deleteLogList: CmdbLog[] = [];

  public columns: Array<Column>;

  public sort: Sort = { name: 'date', order: SortDirection.DESCENDING } as Sort;

  private readonly initLimit: number = 10;
  public limit: number = this.initLimit;

  public readonly initPage: number = 1;
  public page: number = this.initPage;

  public total: number = 0;
  public loading: boolean = false;

  public apiParameters: CollectionParameters = { limit: 10, sort: 'log_time', order: -1, page: 1};

  constructor(private logService: LogService) {
  }

  public ngOnInit(): void {
    this.resetCollectionParameters();
    this.setColumns();
    this.loadDeleted();
  }

  private loadDeleted() {
    const filter = JSON.stringify(this.filterBuilder());
    this.apiParameters = {filter, limit: this.limit, sort: this.sort.name, order: this.sort.order, page: this.page};
    this.logService.getDeleteLogs(this.apiParameters).pipe(takeUntil(this.subscriber))
      .subscribe((apiResponse: APIGetMultiResponse<CmdbLog>) => {
        this.deleteLogList = apiResponse.results;
        this.total = apiResponse.total;
    });
  }

  private resetCollectionParameters(): void {
    this.apiParameters = { limit: 10, sort: 'date', order: -1, page: 1};
  }

  private setColumns(): void {
    const columns = [];
    columns.push({
      display: 'Log ID',
      name: 'public_id',
      data: 'public_id',
      sortable: true,
      searchable: true,
      fixed: true,
      template: this.dataTemplate,
      style: { 'white-space': 'nowrap' },
    } as unknown as Column);

    columns.push({
      display: 'Object ID',
      name: 'object_id',
      data: 'object_id',
      sortable: true,
      searchable: true,
      fixed: true,
      template: this.dataTemplate,
      style: { 'white-space': 'nowrap' },
    } as unknown as Column);

    columns.push({
      display: 'Action',
      name: 'action_name',
      data: 'action_name',
      sortable: true,
      searchable: true,
      fixed: true,
      template: this.dataTemplate,
      cssClasses: ['text-center'],
      style: { width: '6em' }
    } as unknown as Column);

    columns.push({
      display: 'Changes',
      name: 'changes',
      sortable: true,
      searchable: false,
      fixed: true,
      template: this.changeTemplate,
      cssClasses: ['text-center'],
      style: { width: '6em' }
    } as unknown as Column);

    columns.push({
      display: 'Comment',
      name: 'comment',
      data: 'comment',
      sortable: true,
      searchable: false,
      fixed: true,
      template: this.dataTemplate,
      cssClasses: ['text-center'],
      style: { width: '6em' }
    } as unknown as Column);

    columns.push({
      display: 'Author',
      data: 'author_name',
      name: 'author_name',
      sortable: true,
      searchable: true,
      fixed: true,
      template: this.userTemplate,
      cssClasses: ['text-center'],
      style: { width: '6em' }
    } as unknown as Column);

    columns.push({
      display: 'Version',
      name: 'version',
      data: 'version',
      sortable: true,
      searchable: true,
      fixed: true,
      template: this.dataTemplate,
      cssClasses: ['text-center'],
      style: { width: '6em' }
    } as unknown as Column);

    columns.push(
      {
        display: 'Log Time',
        name: 'log_time',
        data: 'log_time',
        sortable: true,
        cssClasses: ['text-center'],
        style: { 'white-space': 'nowrap' },
        template: this.dataTemplate,
        searchable: false,
        render(data: any) {
          const date = new Date(data);
          return new DatePipe('en-US').transform(date, 'dd/MM/yyyy - hh:mm:ss').toString();
        }
      } as Column
    );

    this.columns = columns;
  }

  public onPageChange(page: number) {
    this.page = page;
    this.loadDeleted();
  }

  public onPageSizeChange(limit: number): void {
    this.limit = limit;
    this.loadDeleted();
  }

  public onSortChange(sort: Sort): void {
    this.sort = sort;
    this.loadDeleted();
  }

  public onSearchChange(search: any): void {
    if (search) {
      this.filter = search;
    } else {
      this.filter = undefined;
    }
    this.loadDeleted();
  }

  public onSelectedChange(selectedItems: Array<CmdbLog>): void {
    this.selectedLogIDs = selectedItems.map(m => m.public_id);
  }

  public filterBuilder(): any {
    const query = [];
    if (this.filter) {
      const searchableColumns = this.columns.filter(c => c.searchable);
      const or = [];
      // Searchable Columns
      for (const column of searchableColumns) {
        const regex: any = {};
        regex[column.name] = {
          $regex: String(this.filter),
          $options: 'ismx'
        };
        or.push(regex);
      }
      query.push({
        $addFields: {
          public_id: { $toString: '$public_id' }
        }
      });
      query.push({ $match: { $and: [{log_type: 'CmdbObjectLog'}, {$or: or}]}});
    } else {
      query.push({$match: {log_type: 'CmdbObjectLog'}});
    }
    return query;
  }

  public cleanup() {
    this.cleanUpEmitter.emit(this.selectedLogIDs);
    this.objectsTableComponent.selectedItems = [];
    this.selectedLogIDs = [];
  }

  public ngOnDestroy(): void {
    this.subscriber.next();
    this.subscriber.complete();
  }
}
