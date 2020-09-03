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

import { Component, OnDestroy, OnInit, ViewChild } from '@angular/core';
import { CmdbType } from '../../models/cmdb-type';
import { TypeService } from '../../services/type.service';
import { Subject } from 'rxjs';
import { DataTableDirective } from 'angular-datatables';
import { Router } from '@angular/router';
import { UserService } from '../../../management/services/user.service';
import { FileSaverService } from 'ngx-filesaver';
import { DatePipe } from '@angular/common';
import { FileService } from '../../../export/export.service';
import { NgbModal, NgbModalRef } from '@ng-bootstrap/ng-bootstrap';
import { CleanupModalComponent } from '../builder/modals/cleanup-modal/cleanup-modal.component';

@Component({
  selector: 'cmdb-type-list',
  templateUrl: './type-list.component.html',
  styleUrls: ['./type-list.component.scss']
})
export class TypeListComponent implements OnInit, OnDestroy {

  @ViewChild(DataTableDirective, {static: false})
  public dtElement: DataTableDirective;

  public typeList: CmdbType[] = [];
  public dtOptions: any = {};
  public dtTrigger: Subject<any> = new Subject();
  public selectedObjects: string[] = [];

  // Parameters for CleanUp Modal
  private modalRef: NgbModalRef;

  constructor(private typeService: TypeService, public userService: UserService, private router: Router,
              private fileService: FileService, private fileSaverService: FileSaverService, private datePipe: DatePipe,
              private modalService: NgbModal) {
  }

  public ngOnInit(): void {
    this.dtOptions = {
      ordering: true,
      columnDefs: [ {
        orderable: false,
        className: 'select-checkbox',
        targets:   0
      } ],
      rowCallback: (row: Node, data: any[]) => {
        const self = this;
        $('td:first-child', row).unbind('click');
        $('td:first-child', row).bind('click', () => {
          self.updateDisplay(data[2]);
        });
        return row;
      },
      select: {
        style:    'multi',
        selector: 'td:first-child'
      },
      order: [[1, 'asc']],
      dom:
        '<"row" <"col-sm-2" l><"col" f> >' +
        '<"row" <"col-sm-12"tr>>' +
        '<\"row\" <\"col-sm-12 col-md-5\"i> <\"col-sm-12 col-md-7\"p> >',
      language: {
        search: '',
        searchPlaceholder: 'Filter...'
      }
    };

    this.typeService.getTypeList().subscribe((list: CmdbType[]) => {
        this.typeList = list;
      }, (err) => { console.error(err); },
      () => { this.dtTrigger.next(); });
  }

  public callCleanUpModal(typeInstance: CmdbType): void {
    this.modalRef = this.modalService.open(CleanupModalComponent);
    this.modalRef.componentInstance.typeInstance = typeInstance;
  }

  public ngOnDestroy(): void {
    this.dtTrigger.unsubscribe();
    if (this.modalRef) {
      this.modalRef.close();
    }
  }

  public exportingFiles() {
    if (this.selectedObjects.length === 0 || this.selectedObjects.length === this.typeList.length) {
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
    if ($('.selectAll').is( ':checked' )) {
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
}
