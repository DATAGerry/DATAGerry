/*
* DATAGERRY - OpenSource Enterprise CMDB
* Copyright (C) 2019-2020 NETHINKS GmbH
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

import {Component, Input, OnInit, TemplateRef, ViewChild } from '@angular/core';
import { LogService } from '../../../../services/log.service';
import { CmdbLog } from '../../../../models/cmdb-log';
import { Column, Sort, SortDirection } from '../../../../../layout/table/table.types';
import { CollectionParameters} from '../../../../../services/models/api-parameter';

@Component({
  selector: 'cmdb-object-log-list',
  templateUrl: './object-log-list.component.html',
  styleUrls: ['./object-log-list.component.scss']
})
export class ObjectLogListComponent implements OnInit {

  private id: number;

  @Input()
  set publicID(publicID: number) {
    this.id = publicID;
    if (this.id !== undefined && this.id !== null) {
      this.loadLogList();
    }
  }

  get publicID(): number {
    return this.id;
  }

  @ViewChild('dateTemplate', {static: true}) dateTemplate: TemplateRef<any>;

  @ViewChild('linkTemplate', {static: true}) linkTemplate: TemplateRef<any>;

  @ViewChild('dataTemplate', {static: true}) dataTemplate: TemplateRef<any>;

  @ViewChild('changeTemplate', {static: true}) changeTemplate: TemplateRef<any>;

  @ViewChild('userTemplate', {static: true}) userTemplate: TemplateRef<any>;

  public filter: string;

  public logList: CmdbLog[] = [];

  public columns: Array<Column>;

  public sort: Sort = { name: 'date', order: SortDirection.DESCENDING } as Sort;

  private readonly initLimit: number = 10;
  public limit: number = this.initLimit;

  public readonly initPage: number = 1;
  public page: number = this.initPage;

  public loading: boolean = false;

  public apiParameters: CollectionParameters = { limit: 10, sort: 'date', order: -1, page: 1};

  constructor(private logService: LogService) {
  }

  private loadLogList() {
    this.logService.getLogsByObject(this.publicID).subscribe((logs: CmdbLog[]) => {
      this.logList = logs;
    }, (error) => {
      console.log(error);
    });
  }

  public ngOnInit(): void {
    this.setColumns();
  }

  private setColumns(): void {

    const columns = [];

    columns.push({
      display: 'Date',
      name: 'date',
      data: 'log_time',
      sortable: true,
      searchable: false,
      fixed: true,
      template: this.dateTemplate,
      cssClasses: ['text-center'],
      style: { width: '6em' }
    } as unknown as Column);

    columns.push({
      display: 'Log ID',
      name: 'log-id',
      data: 'public_id',
      sortable: true,
      searchable: false,
      fixed: true,
      template: this.dataTemplate,
      cssClasses: ['text-center'],
      style: { width: '6em' }
    } as unknown as Column);

    columns.push({
      display: 'Action',
      name: 'action',
      data: 'action_name',
      sortable: true,
      searchable: false,
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
      name: 'author',
      sortable: true,
      searchable: false,
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
      searchable: false,
      fixed: true,
      template: this.dataTemplate,
      cssClasses: ['text-center'],
      style: { width: '6em' }
    } as unknown as Column);

    columns.push({
      display: 'Links',
      name: 'links',
      data: 'public_id',
      sortable: true,
      searchable: false,
      fixed: true,
      template: this.linkTemplate,
      cssClasses: ['text-center'],
      style: { width: '6em' }
    } as unknown as Column);

    this.columns = columns;
  }
  public onPageChange(page: number) {
    this.page = page;
  }

  public onPageSizeChange(limit: number): void {
    this.limit = limit;
  }

  public onSortChange(sort: Sort): void {
    this.sort = sort;
  }

  public onSearchChange(search: any): void {
    if (search) {
      this.filter = search;
    } else {
      this.filter = undefined;
    }
  }

}
