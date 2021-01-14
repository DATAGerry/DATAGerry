/*
* DATAGERRY - OpenSource Enterprise CMDB
* Copyright (C) 2019 - 2020 NETHINKS GmbH
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

import { Component, Input, OnDestroy, OnInit, TemplateRef, ViewChild } from '@angular/core';
import { ReplaySubject } from 'rxjs';
import { ObjectService } from '../../../services/object.service';
import { RenderResult } from '../../../models/cmdb-render';
import { APIGetMultiResponse } from '../../../../services/models/api-response';
import { Column, Sort, SortDirection } from '../../../../layout/table/table.types';
import { CollectionParameters } from '../../../../services/models/api-parameter';
import { takeUntil } from 'rxjs/operators';
import { DatePipe } from '@angular/common';
import { SupportedExporterExtension } from '../../../../export/export-objects/model/supported-exporter-extension';
import { FileSaverService } from 'ngx-filesaver';
import { FileService } from '../../../../export/export.service';

@Component({
  selector: 'cmdb-object-references-table',
  templateUrl: './object-references-table.component.html',
  styleUrls: ['./object-references-table.component.scss']
})
export class ObjectReferencesTableComponent implements OnInit, OnDestroy {

  /**
   * Table Template: active column.
   */
  @ViewChild('activeTemplate', { static: true }) activeTemplate: TemplateRef<any>;

  /**
   * Table Template: Type name column.
   */
  @ViewChild('typeNameTemplate', { static: true }) typeNameTemplate: TemplateRef<any>;

  /**
   * Table Template: Link action column.
   */
  @ViewChild('actionTemplate', { static: true }) actionTemplate: TemplateRef<any>;

  /**
   * Table Template: Link action column.
   */
  @ViewChild('exportButtonTemplate', { static: true }) exportButtonTemplate: TemplateRef<any>;


  /**
   * Global un-subscriber for http calls to the rest backend.
   */
  private subscriber: ReplaySubject<void> = new ReplaySubject<void>();

  /**
   * ID of the referenced object.
   */
  public publicID: number;

  /**
   * ID setter of the referenced object.
   * @param id
   */
  @Input('publicID') public set PublicID(id: number) {
    this.publicID = id;
    this.loadObjectsFromAPI();
  }

  /**
   * Table columns definition.
   */
  public columns: Array<Column>;

  public refererObjects: Array<RenderResult> = [];
  public refererAPIResponse: APIGetMultiResponse<RenderResult>;
  public totalReferer: number = 0;

  /**
   * Referer selection.
   */
  public selectedObjects: Array<RenderResult> = [];
  public selectedObjectIDs: Array<number> = [];


  /**
   * Max number of objects per site.
   * @private
   */
  private readonly initLimit: number = 10;
  public limit: number = this.initLimit;

  /**
   * Begin with first page.
   */
  public readonly initPage: number = 1;
  public page: number = this.initPage;

  /**
   * Default sort filter.
   */
  public sort: Sort = { name: 'public_id', order: SortDirection.DESCENDING } as Sort;

  /**
   * Loading indicator.
   */
  public loading: boolean = false;

  /**
   * Possible export formats.
   */
  public formatList: Array<SupportedExporterExtension> = [];


  constructor(private objectService: ObjectService, private datePipe: DatePipe,
              private fileSaverService: FileSaverService, private fileService: FileService) {
    this.fileService.callFileFormatRoute().subscribe(data => {
      this.formatList = data;
    });
  }

  public ngOnInit(): void {
    this.columns = [
      {
        display: 'Active',
        name: 'active',
        data: 'object_information.active',
        sortable: true,
        template: this.activeTemplate,
        cssClasses: ['text-center'],
        style: { width: '6rem' }
      },
      {
        display: 'Public ID',
        name: 'public_id',
        data: 'object_information.object_id',
        sortable: true
      },
      {
        display: 'Type',
        name: 'type_id',
        data: 'type_information.type_name',
        sortable: true,
        template: this.typeNameTemplate,
      },
      {
        display: 'Creation Time',
        name: 'creation_time',
        data: 'object_information.creation_time',
        sortable: true,
        searchable: false,
        render(data: any) {
          const date = new Date(data);
          return new DatePipe('en-US').transform(date, 'dd/MM/yyyy - hh:mm:ss').toString();
        }
      },
      {
        display: 'Actions',
        name: 'actions',
        data: 'object_information.object_id',
        template: this.actionTemplate,
        sortable: false,
        fixed: true,
        cssClasses: ['text-center'],
        cellClasses: ['actions-buttons'],
        style: { width: '6rem' }
      },
    ] as Array<Column>;
  }

  /**
   * Load/reload objects from the api.
   * @private
   */
  private loadObjectsFromAPI(): void {
    this.loading = true;

    const params: CollectionParameters = {
      filter: undefined, limit: this.limit,
      sort: this.sort.name, order: this.sort.order, page: this.page
    };

    this.objectService.getObjectReferences(this.publicID, params).pipe(takeUntil(this.subscriber)).subscribe(
      (apiResponse: APIGetMultiResponse<RenderResult>) => {
        this.refererAPIResponse = apiResponse;
        this.refererObjects = apiResponse.results as Array<RenderResult>;
        this.totalReferer = apiResponse.total;
        this.loading = false;
      });
  }


  /**
   * On table sort change.
   * Reload all objects.
   *
   * @param sort
   */
  public onSortChange(sort: Sort): void {
    this.sort = sort;
    this.loadObjectsFromAPI();
  }

  /**
   * On table page change.
   * Reload all objects.
   *
   * @param page
   */
  public onPageChange(page: number) {
    this.page = page;
    this.loadObjectsFromAPI();
  }

  /**
   * On table page size change.
   * Reload all objects.
   *
   * @param limit
   */
  public onPageSizeChange(limit: number): void {
    this.limit = limit;
    this.loadObjectsFromAPI();
  }

  /**
   * On table selection change.
   * Map selected items by the object id
   *
   * @param selectedItems
   */
  public onSelectedChange(selectedItems: Array<RenderResult>): void {
    this.selectedObjects = selectedItems;
    this.selectedObjectIDs = selectedItems.map(t => t.object_information.object_id);
  }

  /**
   * Exports the referenceList as zip
   *
   * @param see the filetype to be zipped
   */
  public exportingFiles(see: SupportedExporterExtension) {
    if (this.selectedObjects.length !== 0) {
      const exportApi: CollectionParameters = {
        filter: {public_id: {$in: this.selectedObjectIDs}},
        optional: {classname: see.extension, zip: true}
      };
      this.fileService.callExportRoute(exportApi)
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

  /**
   * Unsubscribe all on component destroy.
   */
  public ngOnDestroy(): void {
    this.subscriber.next();
    this.subscriber.complete();
  }

}
