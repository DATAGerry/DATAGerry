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


import { Component, OnDestroy, ViewChild, Input, OnInit } from '@angular/core';
import { DataTableDirective } from 'angular-datatables';
import { BehaviorSubject, Subject} from 'rxjs';
import { UserService } from '../../../management/services/user.service';
import { ApiCallService } from '../../../services/api-call.service';
import { DatePipe } from '@angular/common';

import { Router } from '@angular/router';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { ModalComponent } from '../../helpers/modal/modal.component';
import { FileSaverService } from 'ngx-filesaver';
import { TableColumn} from './models/table-column';
import { TableColumnAction} from './models/table-columns-action';
import { RenderResult } from '../../../framework/models/cmdb-render';
import { FileService } from '../../../export/export.service';

@Component({
  selector: 'cmdb-table',
  templateUrl: './table.component.html',
  styleUrls: ['./table.component.scss'],
  providers: [DatePipe]
})
export class TableComponent implements OnInit, OnDestroy {

  @ViewChild(DataTableDirective, {static: false})
  public dtElement: DataTableDirective;
  public dtOptions: any;
  public dtTrigger: Subject<any> = new Subject();

  @Input() thColumns: TableColumn[];
  @Input() thColumnsActions: TableColumnAction[];
  @Input() add: {};
  @Input() print: {};
  @Input() dtButtons: any[];

  @Input() pageTitle: string = 'List';
  @Input() linkRoute: string = 'object/';
  @Input() showExport: boolean = true;
  @Input() showDeleteSelected: boolean = true;

  public items: any = new BehaviorSubject<RenderResult[]>([]);
  public formatList: any[] = [];

  constructor(private userService: UserService, private apiCallService: ApiCallService,
              private fileService: FileService, private router: Router,
              private modalService: NgbModal, private fileSaverService: FileSaverService,
              private datePipe: DatePipe) {
    this.add = {
      // add new
      text: '<i class="fas fa-plus"></i> Add',
      className: 'btn btn-success btn-sm mr-1',
      action: function() {
        this.router.navigate(['/framework/' + this.linkRoute + 'add']);
      }.bind(this)
    };

    this.print = {
      // print
      text: 'Print <i class="fas fa-print"></i>',
      extend: 'print',
      className: 'btn btn-info btn-sm mr-1'
    };

    this.thColumns = [
      { name: 'id', label: 'ID'},
      { name: 'type', label: 'Type'},
      { name: 'author', label: 'Author'},
      { name: 'create_time', label: 'Creation Time'},
      { name: 'action', label: 'Action'}];

    this.thColumnsActions = [
      { name: 'view', classValue: 'text-dark ml-1', linkRoute: '', fontIcon: 'eye', active: false},
      { name: 'edit', classValue: 'text-dark ml-1', linkRoute: 'edit/', fontIcon: 'edit'},
      { name: 'delete', classValue: 'text-dark ml-1', linkRoute: 'delete/', fontIcon: 'trash'}];
  }

  ngOnInit(): void {
    if (this.showExport) {
      this.fileService.callFileFormatRoute().subscribe( data => {
        this.formatList = data;
      });
    }
  }

  @Input() set entryLists(value: RenderResult[]) {
    this.items.next(value);
    this.buildTable();
    this.dtTrigger.next();
  }

  get entryLists(): RenderResult[] {
    return this.items.getValue();
  }

  private buildButtons() {
    this.dtButtons = [];
    if (Object.keys(this.add).length !== 0) {
      this.dtButtons.push(this.add);
    }
    if (Object.keys(this.print).length !== 0) {
      this.dtButtons.push(this.print);
    }
  }

  private buildOptions(buttons) {
    this.dtOptions = {
      ordering: true,
      order: [[1, 'asc']],
      columnDefs: [{
        targets: 'nosort',
        orderable: false,
      }],
      retrieve: true,
      language: {
        search: '',
        searchPlaceholder: 'Filter...'
      },
      dom:
        '<"row" <"col-sm-2" l> <"col-sm-3" B > <"col" f> >' +
        '<"row" <"col-sm-12"tr>>' +
        '<\"row\" <\"col-sm-12 col-md-5\"i> <\"col-sm-12 col-md-7\"p> >',
      // Configure the buttons
      // Declare the use of the extension in the dom parameter
      buttons: {
        dom: {
          container: {
            className: 'dt-buttons btn-groups btn-groups-sm'
          }
        },
        buttons,
      },
    };
  }

  private buildTable() {
    this.buildButtons();
    this.buildOptions(this.dtButtons);
  }

  ngOnDestroy(): void {
    // Do not forget to unsubscribe the event
    this.dtTrigger.unsubscribe();
  }

  public rerender(): void {
    if (typeof this.dtElement !== 'undefined' && typeof this.dtElement.dtInstance !== 'undefined') {
      this.dtElement.dtInstance.then((dtInstance: DataTables.Api) => {
        // Destroy the table first
        dtInstance.destroy();
      });
    }
  }

  public selectAll() {
    const overall: any = document.getElementsByClassName('select-all-checkbox')[0];
    const allCheckbox: any = document.getElementsByClassName('select-checkbox');
    const checking = overall.checked;
    for (const box of allCheckbox) {
      box.checked = checking;
    }
  }

  public updateDisplay() {
    const overall: any = document.getElementsByClassName('select-all-checkbox')[0];
    const allCheckbox: any = document.getElementsByClassName('select-checkbox');
    let checkedCount = 0;
    for (const box of allCheckbox) {
      if (box.checked) {
        checkedCount++;
      }
    }

    if (checkedCount === 0) {
      overall.checked = false;
      overall.indeterminate = false;
    } else if (checkedCount === allCheckbox.length) {
      overall.checked = true;
      overall.indeterminate = false;
    } else {
      overall.checked = false;
      overall.indeterminate = true;
    }
  }

  public delManyObjects() {
    const allCheckbox: any = document.getElementsByClassName('select-checkbox');
    const publicIds: number[] = [];
    for (const box of allCheckbox) {
      if (box.checked && box.id) {
        publicIds.push(box.id);
      }
    }

    if (publicIds.length > 0) {
      const modalComponent = this.modalService.open(ModalComponent);
      modalComponent.componentInstance.title = 'Delete selected Objects';
      modalComponent.componentInstance.modalMessage = 'Are you sure, you want to delete all selected objects?';
      modalComponent.componentInstance.buttonDeny = 'Cancel';
      modalComponent.componentInstance.buttonAccept = 'Delete';

      modalComponent.result.then((result) => {
        if (result) {
          this.apiCallService.callDeleteManyRoute(this.linkRoute + 'delete/' + publicIds ).subscribe(data => {
            this.apiCallService.callGetRoute('render/').subscribe((objs: RenderResult[]) => {
              this.items.next(objs);
            });
          });
        }
      }, (reason) => {
        // ToDO:
      });
    }
  }

  public delObject(route: any, value: RenderResult) {
    if ( route === 'delete/') {
      this.router.navigate([this.router.url + '/' + route + value.type_information.type_id]);
    }

    if ( route === 'object/') {
      const modalComponent = this.createModal(
        'Delete Object',
        'Are you sure you want to delete this Object?',
        'Cancel',
        'Delete');

      modalComponent.result.then((result) => {
        if (result) {
          const id = value.object_information.object_id;
          this.apiCallService.callDeleteRoute(this.linkRoute + id).subscribe(data => {
            this.apiCallService.callGetRoute('object/').subscribe((objs: RenderResult[]) => {
              this.items.next(objs);
              this.rerender();
              this.dtTrigger.next();
            });
          });
        }
      }, (reason) => {
        // ToDO:
      });
    }
  }

  public exporter(exportType: any) {
    const allCheckbox: any = document.getElementsByClassName('select-checkbox');
    const publicIds: string[] = [];
    for (const box of allCheckbox) {
      if (box.checked && box.id) {
        publicIds.push(box.id);
      }
    }
    if (publicIds.length > 0) {
      this.fileService.callExportRoute('/file/object/' + publicIds.toString(), exportType.id)
        .subscribe(res => this.downLoadFile(res, exportType));
    }
  }

  public downLoadFile(data: any, exportType: any) {
    const timestamp = this.datePipe.transform(new Date(), 'MM_dd_yyyy_hh_mm_ss');
    this.fileSaverService.save(data.body, timestamp + '.' + exportType.label);
  }

  private createModal(title: string, modalMessage: string, buttonDeny: string, buttonAccept: string) {
    const modalComponent = this.modalService.open(ModalComponent);
    modalComponent.componentInstance.title = title;
    modalComponent.componentInstance.modalMessage = modalMessage;
    modalComponent.componentInstance.buttonDeny = buttonDeny;
    modalComponent.componentInstance.buttonAccept = buttonAccept;
    return modalComponent;
  }
}
