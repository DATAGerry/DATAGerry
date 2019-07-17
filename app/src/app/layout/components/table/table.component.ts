/*
* dataGerry - OpenSource Enterprise CMDB
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


import { Component, OnDestroy, ViewChild, Input } from '@angular/core';
import { DataTableDirective } from 'angular-datatables';
import { BehaviorSubject, Subject} from 'rxjs';
import { UserService } from '../../../user/services/user.service';
import { ApiCallService } from '../../../services/api-call.service';
import { HttpHeaders } from '@angular/common/http';
import { DatePipe } from '@angular/common';
import { ExportService } from '../../../services/export.service';
import { Router } from '@angular/router';

@Component({
  selector: 'cmdb-table',
  templateUrl: './table.component.html',
  styleUrls: ['./table.component.scss'],
  providers: [DatePipe]
})
export class TableComponent implements OnDestroy {

  @ViewChild(DataTableDirective, {static: false})
  public dtElement: DataTableDirective;
  public dtOptions: any = {}; // : DataTables.Settings = {};
  public dtTrigger: Subject<any> = new Subject();

  /**
   * overwrite default value for edit Button (table-toolbar)
   */
  @Input() pageTitle: string = 'List';

  /**
   * overwrite default value for add Button (table-toolbar)
   */
  @Input() add: {} = {
    // add new
    text: '<i class="fa fa-plus" aria-hidden="true"></i> Add',
    className: 'btn btn-success btn-sm mr-1'
  };

  /**
   * overwrite default value for print Button (table-toolbar)
   */
  @Input() print: {} = {
    // print
    text: 'Print <i class="fa fa-print" aria-hidden="true"></i>',
    extend: 'print',
    className: 'btn btn-info btn-sm mr-1'
  };

  /**
   * overwrite default value for all Buttons (table-toolbar)
   */
  @Input() dtButtons: any[] = [];

  /**
   * overwrite default value for routeLink (defaul : '/framework/object/')
   */
  @Input() linkRoute: string = 'object/';

  public items: any = new BehaviorSubject<any[]>([]);

  constructor(private userService: UserService, private apiCallService: ApiCallService,
              private exportService: ExportService, private router: Router) {
    this.add = {
      // add new
      text: '<i class="fa fa-plus" aria-hidden="true"></i> Add',
      className: 'btn btn-success btn-sm mr-1',
      action: function() {
        this.router.navigate(['/framework/' + this.linkRoute + 'add']);
      }.bind(this)
    };
  }

  @Input() set entryLists(value: any[]) {
    this.items.next(value);
    this.buildTable();
    this.rerender();
    this.dtTrigger.next();
  }

  get entryLists(): any[] {
    return this.items.getValue();
  }

  private buildButtons() {
    this.dtButtons.length = 0;
    this.dtButtons.push(this.add);
    this.dtButtons.push(this.print);
  }

  private buildOptions(buttons) {
    this.dtOptions = {
      ordering: true,
      order: [[2, 'asc']],
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
            className: 'dt-buttons btn-group btn-group-sm'
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
      this.apiCallService.callDeleteManyRoute(this.linkRoute + 'delete/' + publicIds ).subscribe(data => {
        this.apiCallService.callGetRoute(this.linkRoute).subscribe(objs => {
          this.entryLists = objs;
        });
      });
    }
  }

  public delObject(value: any) {
    const id = value.public_id;
    this.apiCallService.callDeleteRoute(this.linkRoute + id).subscribe(data => {
      this.apiCallService.callGetRoute(this.linkRoute).subscribe(objs => {
        this.entryLists = objs;
      });
    });
  }

  public exporter(fileExtension: string) {

    const allCheckbox: any = document.getElementsByClassName('select-checkbox');
    const publicIds: string[] = [];

    for (const box of allCheckbox) {
      if (box.checked && box.id) {
        publicIds.push(box.id);
      }
    }

    const httpHeader = new HttpHeaders({
      'Content-Type': 'application/' + fileExtension
    });

    if (publicIds.length > 0) {
      this.exportService.callExportRoute('export/' + fileExtension + '/' + this.linkRoute + publicIds,
        fileExtension,
        httpHeader);
    }
  }
}
