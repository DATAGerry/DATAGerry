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

import {Component, Input, OnDestroy, OnInit, TemplateRef, ViewChild} from '@angular/core';
import { Subject } from 'rxjs';
import { RenderResult } from '../../../../models/cmdb-render';
import { ObjectService } from '../../../../services/object.service';
import { DataTableDirective } from 'angular-datatables';
import { FileService } from '../../../../../export/export.service';
import { DatePipe } from '@angular/common';
import { FileSaverService } from 'ngx-filesaver';
import { ExportObjectsFileExtension } from '../../../../../export/export-objects/model/export-objects-file-extension';
import {CmdbType} from '../../../../models/cmdb-type';
import {Column, Sort, SortDirection} from '../../../../../layout/table/table.types';

@Component({
  selector: 'cmdb-object-reference-list',
  templateUrl: './object-reference-list.component.html',
  styleUrls: ['./object-reference-list.component.scss']
})
export class ObjectReferenceListComponent implements OnInit, OnDestroy {

  private id: number;

  @ViewChild('objectTemplate', {static: true}) objectTemplate: TemplateRef<any>;

  @ViewChild('typeTemplate', {static: true}) typeTemplate: TemplateRef<any>;

  @ViewChild('summaryTemplate', {static: true}) summaryTemplate: TemplateRef<any>;

  @ViewChild('linkTemplate', {static: true}) linkTemplate: TemplateRef<any>;

  public columns: Column[];

  public sort: Sort = { name: 'public_id', order: SortDirection.DESCENDING } as Sort;

  public readonly initPage: number = 1;
  public page: number = this.initPage;

  private readonly initLimit: number = 25;
  public limit: number = this.initLimit;

  public loading: boolean = false;

  private filter: string;

  public referenceList: RenderResult[] = [];
  public formatList: ExportObjectsFileExtension[] = [];

  @Input()
  set publicID(publicID: number) {
    this.id = publicID;
    if (this.id !== undefined && this.id !== null) {
      this.loadObjectReferences();
    }
  }

  get publicID(): number {
    return this.id;
  }

  public constructor(private objectService: ObjectService, private datePipe: DatePipe,
                     private fileSaverService: FileSaverService, private fileService: FileService) {
    this.fileService.callFileFormatRoute().subscribe(data => {
      this.formatList = data;
    });
  }

  ngOnInit(): void {
        this.setColumns();
  }

  private loadObjectReferences() {
    this.objectService.getObjectReferences(this.publicID).subscribe((references: RenderResult[]) => {
        this.referenceList = references;
      },
      (error) => {
        console.error(error);
      },
      () => {
      });
  }

  /**
   * Exports the referenceList as zip
   *
   * @param exportType the filetype to be zipped
   */
  public exportingFiles(exportType: ExportObjectsFileExtension) {
    if (this.referenceList.length !== 0) {
      const objectIDs: number[] = [];
      for (const el of this.referenceList) {
        objectIDs.push(el.object_information.object_id);
      }
      this.fileService.callExportRoute(objectIDs, exportType.extension, true)
        .subscribe(res => this.downLoadFile(res));
    }
  }

  /**
   * Downloads file
   * @param data the file data to be downloaded
   */
  public downLoadFile(data: any) {
    const timestamp = this.datePipe.transform(new Date(), 'MM_dd_yyyy_hh_mm_ss');
    this.fileSaverService.save(data.body, timestamp + '.' + 'zip');
  }

  private setColumns(): void {
    const columns = [];

    columns.push({
      display: 'Object ID',
      name: 'object-id',
      data: 'object_information.object_id',
      sortable: true,
      searchable: false,
      fixed: true,
      template: this.objectTemplate,
      cssClasses: ['text-center'],
      style: { width: '6em' }
    } as unknown as Column);

    columns.push({
      display: 'Type',
      name: 'actions',
      data: 'type_information',
      sortable: true,
      searchable: false,
      fixed: true,
      template: this.typeTemplate,
      cssClasses: ['text-center'],
      style: { width: '6em' }
    } as unknown as Column);

    columns.push({
      display: 'Summary',
      name: 'summary',
      sortable: true,
      searchable: false,
      fixed: true,
      template: this.summaryTemplate,
      cssClasses: ['text-center'],
      style: { width: '6em' }
    } as unknown as Column);

    columns.push({
      display: 'Link',
      name: 'link',
      data: 'object_information.object_id',
      sortable: true,
      searchable: false,
      fixed: true,
      template: this.linkTemplate,
      cssClasses: ['text-center'],
      style: { width: '6em' }
    } as unknown as Column);

    this.columns = columns;
  }


  /**
   * On table page change.
   * Reload all objects.
   *
   * @param page
   */
  public onPageChange(page: number) {
    this.page = page;
  }

  /**
   * On table page size change.
   * Reload all objects.
   *
   * @param limit
   */
  public onPageSizeChange(limit: number): void {
    this.limit = limit;
  }

  /**
   * On table sort change.
   * Reload all objects.
   *
   * @param sort
   */
  public onSortChange(sort: Sort): void {
    this.sort = sort;
  }

  /**
   * On table search change.
   * Reload all objects.
   *
   * @param search
   */
  public onSearchChange(search: any): void {
    if (search) {
      this.filter = search;
    } else {
      this.filter = undefined;
    }
  }

  public ngOnDestroy(): void {
  }
}
