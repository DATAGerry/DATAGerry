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


import {Component, OnDestroy, OnInit, ViewChild, Input, OnChanges, SimpleChanges} from '@angular/core';
import {DataTableDirective} from 'angular-datatables';
import {Subject} from 'rxjs';
import {UserService} from '../../../user/services/user.service';

@Component({
  selector: 'cmdb-table',
  templateUrl: './table.component.html',
  styleUrls: ['./table.component.scss']
})
export class TableComponent implements OnInit, OnDestroy, OnChanges {

  @ViewChild(DataTableDirective, {static: false})
  public dtElement: DataTableDirective;
  public dtOptions: any = {}; // : DataTables.Settings = {};
  public dtTrigger: Subject<any> = new Subject();

  /**
   * iterable entries for table. Type independent
   */
  @Input() entryLists: any[] = [];

  /**
   * Create advanced fields and only display if extended fields exist
   */
  @Input() extendedFields: any[] = [];

  /**
   * overwrite default value for add Button (table-toolbar)
   */
  @Input() add: {} = {
    // add new
    text: '<i class="fa fa-file-o" aria-hidden="true"></i>',
    className: 'btn btn-light',
  };

  /**
   * overwrite default value for edit Button (table-toolbar)
   */
  @Input() edit: {} = {
    // edit
    text: '<i class="fa fa-pencil-square-o" aria-hidden="true"></i>',
    className: 'btn btn-light',
  };

  /**
   * overwrite default value for copy Button (table-toolbar)
   */
  @Input() copy: {} = {
    // copy
    text: '<i class="fa fa-files-o" aria-hidden="true"></i>',
    extend: 'copy',
    className: 'btn btn-light'
  };

  /**
   * overwrite default value for delete Button (table-toolbar)
   */
  @Input() delete: {} = {
    // delete
    text: '<i class="fa fa-trash-o" aria-hidden="true"></i>',
    className: 'btn btn-light',
  };

  /**
   * overwrite default value for print Button (table-toolbar)
   */
  @Input() print: {} = {
    // print
    text: '<i class="fa fa-print" aria-hidden="true"></i>',
    extend: 'print',
    className: 'btn btn-light'
  };

  /**
   * overwrite default value for export Button (table-toolbar)
   */
  @Input() export: {} = {
    // export to exel
    text: '<i class="fa fa-file-excel-o" aria-hidden="true"></i>',
    extend: 'excel',
    className: 'btn btn-light'
  };

  /**
   * overwrite default value for all Buttons (table-toolbar)
   */
  @Input() dtButtons: any[] = [];

  /**
   * overwrite default value for routeLink (defaul : '/framework/object/')
   */
  @Input() linkRoute: string = '/framework/object/';

  constructor(private userService: UserService) {
  }

  ngOnInit() {
    this.buildTable();
  }

  ngOnChanges(changes: SimpleChanges): void {
    this.dtTrigger.next();
  }

  private buildButtons() {
    if (this.dtButtons.length === 0) {
      this.dtButtons.push(this.add);
      this.dtButtons.push(this.edit);
      this.dtButtons.push(this.copy);
      this.dtButtons.push(this.delete);
      this.dtButtons.push(this.print);
      this.dtButtons.push(this.export);
    }
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
        '<"row" <"col-sm-3" l> <"col-sm-3" B > <"col" f> >' +
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
}
