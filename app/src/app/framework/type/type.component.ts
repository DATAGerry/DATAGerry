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

import { AfterViewInit, Component, OnDestroy, OnInit, ViewChild } from '@angular/core';
import { TypeService } from '../services/type.service';
import { DataTableDirective } from 'angular-datatables';
import { takeUntil } from 'rxjs/operators';
import { ReplaySubject, Subject } from 'rxjs';
import { APIGetMultiResponse } from '../../services/models/api-response';
import { CmdbType } from '../models/cmdb-type';
import { CollectionParameters } from '../../services/models/api-parameter';
import { NgbModal, NgbModalRef } from '@ng-bootstrap/ng-bootstrap';
import { Router } from '@angular/router';
import { FileSaverService } from 'ngx-filesaver';
import { CleanupModalComponent } from './builder/modals/cleanup-modal/cleanup-modal.component';
import { DatePipe } from '@angular/common';
import { FileService } from '../../export/export.service';

@Component({
  selector: 'cmdb-type',
  templateUrl: './type.component.html',
  styleUrls: ['./type.component.scss']
})
export class TypeComponent implements OnInit, AfterViewInit, OnDestroy {

  /**
   * Datatable datas
   */
  public dtOptions: any = {};
  public dtTrigger: Subject<void> = new Subject();
  @ViewChild(DataTableDirective, { static: false }) dtElement: DataTableDirective;

  /**
   * Global unsubscriber for http calls to the rest backend.
   */
  private unSubscribe: ReplaySubject<void> = new ReplaySubject();

  /**
   * Current category collection
   */
  public types: Array<CmdbType>;
  public typesAPIResponse: APIGetMultiResponse<CmdbType>;

  /**
   * Selection parameters
   */
  public selected: Array<number> = [];
  public all: boolean = false;
  public remove: boolean = false;
  public update: boolean = false;

  /**
   * Export modal
   */
  private modalRef: NgbModalRef;

  constructor(private typeService: TypeService, private router: Router, private fileService: FileService,
              private fileSaverService: FileSaverService, private modalService: NgbModal, private datePipe: DatePipe) {
    this.types = [];
  }

  /**
   * Starts the component and init the table
   */
  public ngOnInit(): void {
    this.dtOptions = {
      ordering: true,
      columnDefs: [
        {
          orderable: true,
          searchable: true,
          targets: [1, 2, 3]
        },
        {
          name: 'active',
          targets: [1]
        },
        {
          name: 'public_id',
          targets: [2]
        },
        {
          name: 'name',
          targets: [3]
        },
        {
          name: 'creation_time',
          targets: [4],
          orderable: true,
          searchable: false
        },
        {
          orderable: false,
          searchable: false,
          targets: [0, 5, 6]
        }
      ],
      language: {
        search: '',
        searchPlaceholder: 'Filter...'
      },
      order: [[2, 'desc']],
      dom:
        '<"row" <"col-sm-2" l><"col" f> >' +
        '<"row" <"col-sm-12"tr>>' +
        '<\"row\" <\"col-sm-12 col-md-5\"i> <\"col-sm-12 col-md-7\"p> >',
      searching: true,
      serverSide: true,
      processing: true,
      ajax: (params: any, callback) => {
        let filter;
        if (params.search.value !== '') {
          const searchableColumns = params.columns.filter(column => {
            return column.searchable === true;
          });

          const columnQueries = [];
          for (const column of searchableColumns) {
            const regex = {
              $regexMatch: {
                input: { $toString: `$${ column.name }` },
                regex: params.search.value,
                options: 'ismx'
              }
            };
            columnQueries.push(regex);
          }
          const query = [
            { $addFields: { match: { $or: columnQueries } } },
            { $match: { match: true } },
            { $project: { match: 0 } }
          ];
          filter = JSON.stringify(query);
        }

        const apiParameters: CollectionParameters = {
          filter,
          page: Math.ceil(params.start / params.length) + 1,
          limit: params.length,
          sort: params.columns[params.order[0].column].name,
          order: params.order[0].dir === 'desc' ? -1 : 1,
        };

        this.typeService.getTypesIteration(apiParameters).pipe(
          takeUntil(this.unSubscribe)).subscribe(
          (response: APIGetMultiResponse<CmdbType>) => {
            this.typesAPIResponse = response;
            this.types = this.typesAPIResponse.results;
            callback({
              recordsTotal: response.total,
              recordsFiltered: response.total,
              data: []
            });
          });
      }
    };
  }

  /**
   * Trigger the table render after init the data
   */
  public ngAfterViewInit(): void {
    this.dtTrigger.next();
  }

  /**
   * Destroy subscriptions after clsoe
   */
  public ngOnDestroy(): void {
    this.dtTrigger.unsubscribe();
    if (this.modalRef) {
      this.modalRef.close();
    }
    this.unSubscribe.next();
    this.unSubscribe.complete();
  }

  /**
   * Open the clean modal
   * @param typeInstance - Instance of the type which will be cleaned
   */
  public callCleanUpModal(typeInstance: CmdbType): void {
    this.modalRef = this.modalService.open(CleanupModalComponent);
    this.modalRef.componentInstance.typeInstance = typeInstance;
  }

  /**
   * Call the export routes with the selected types
   */
  public exportingFiles() {
    if (this.selected.length === 0 || this.selected.length === this.types.length) {
      this.fileService.getTypeFile()
        .subscribe(res => this.downLoadFile(res, 'json'));
    } else {
      this.fileService.callExportTypeRoute('/export/type/' + this.selected.toString())
        .subscribe(res => this.downLoadFile(res, 'json'));
    }
  }

  /**
   * Download the selected export file
   *
   * @param data Data which will be exported
   * @param exportType File extension
   */
  public downLoadFile(data: any, exportType: any) {
    const timestamp = this.datePipe.transform(new Date(), 'MM_dd_yyyy_hh_mm_ss');
    this.fileSaverService.save(data.body, timestamp + '.' + exportType);
  }

  /**
   * Select all types in the table
   */
  public selectAll() {
    if (this.all) {
      this.selected = [];
      this.all = false;
    } else {
      this.selected = [];
      for (const type of this.types) {
        this.selected.push(type.public_id);
      }
      this.all = true;
    }
  }

  /**
   * Toggle a specific selection in the table.
   * Disables the `all` selection in the headline.
   *
   * @param publicID ID of the row/type
   */
  public toggleSelection(publicID: number) {
    const idx = this.selected.indexOf(publicID);
    if (idx === -1) {
      this.selected.push(publicID);
    } else {
      this.selected.splice(idx, 1);
      this.all = false;
    }
  }

  /**
   * Quickhack to open the selection box.
   */
  public showAlert(): void {
    $('#infobox').show();
  }

}
