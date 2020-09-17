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

  public selectedObjects: string[] = [];

  private modalRef: NgbModalRef;

  constructor(private typeService: TypeService, private router: Router, private fileService: FileService,
              private fileSaverService: FileSaverService, private modalService: NgbModal, private datePipe: DatePipe) {
    this.types = [];
  }

  public ngOnInit(): void {
    this.dtOptions = {
      /*columns: [
        {
          title: '<input type="checkbox" class="selectAll" name="selectAll" value="all" (click)="selectAll()">',
          name: 'all',
          orderable: false,
          data: '',
          className: 'select-checkbox',
          targets: 0
        },
        {
          title: 'Active',
          name: 'active',
          data: 'active',
        },
        {
          title: 'PublicID',
          name: 'public_id',
          data: 'public_id'
        },
        {
          title: 'Name',
          name: 'name',
          data: 'name'
        },
        {
          title: 'Creation Time',
          name: 'creation_time',
          data: 'creation_time',
        },
        {
          title: 'Actions',
          name: 'actions',
        },
        {
          title: 'Cleanup',
          name: 'cleanup',
          data: 'clean_db'
        }
      ],*/
      columnDefs: [
        {
          orderable: false,
          className: 'select-checkbox',
          targets: 0
        },
        {
          orderable: false,
          targets: [1, 5, 6]
        }
      ],
      rowCallback: (row: Node, data: any[]) => {
        $('td:first-child', row).unbind('click');
        $('td:first-child', row).bind('click', () => {
          this.updateDisplay(data[2]);
        });
        return row;
      },
      select: {
        style: 'multi',
        selector: 'td:first-child'
      },
      ordering: true,
      order: [[2, 'desc']],
      dom:
        '<"row" <"col-sm-2" l><"col" f> >' +
        '<"row" <"col-sm-12"tr>>' +
        '<\"row\" <\"col-sm-12 col-md-5\"i> <\"col-sm-12 col-md-7\"p> >',
      searching: false,
      serverSide: true,
      processing: true,
      ajax: (params: any, callback) => {
        const apiParameters: CollectionParameters = {
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

  public ngAfterViewInit(): void {
    this.dtTrigger.next();
  }

  public ngOnDestroy(): void {
    this.dtTrigger.unsubscribe();
    if (this.modalRef) {
      this.modalRef.close();
    }
    this.unSubscribe.next();
    this.unSubscribe.complete();
  }

  public callCleanUpModal(typeInstance: CmdbType): void {
    this.modalRef = this.modalService.open(CleanupModalComponent);
    this.modalRef.componentInstance.typeInstance = typeInstance;
  }

  public exportingFiles() {
    if (this.selectedObjects.length === 0 || this.selectedObjects.length === this.types.length) {
      this.fileService.getTypeFile()
        .subscribe(res => this.downLoadFile(res, 'json'));
    } else {
      this.fileService.callExportTypeRoute('/export/type/' + this.selectedObjects.toString())
        .subscribe(res => this.downLoadFile(res, 'json'));
    }
  }

  public downLoadFile(data: any, exportType: any) {
    const timestamp = this.datePipe.transform(new Date(), 'MM_dd_yyyy_hh_mm_ss');
    this.fileSaverService.save(data.body, timestamp + '.' + exportType);
  }

  public selectAll() {
    const table: any = $('#type-list-datatable');
    const dataTable: any = table.DataTable();
    const rows: any = dataTable.rows();
    this.selectedObjects = [];
    if ($('.selectAll').is(':checked')) {
      rows.select();
      let lenx: number = rows.data().length - 1;
      while (lenx >= 0) {
        this.selectedObjects.push(rows.data()[lenx][2]);
        lenx--;
      }
    } else {
      rows.deselect();
    }
  }

  public updateDisplay(publicID: string): void {
    const index = this.selectedObjects.findIndex(d => d === publicID); // find index in your array
    if (index > -1) {
      this.selectedObjects.splice(index, 1); // remove element from array
    } else {
      this.selectedObjects.push(publicID);
    }
  }

  public showAlert(): void {
    $('#infobox').show();
  }

}
