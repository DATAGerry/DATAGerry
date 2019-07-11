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


import { Component, OnDestroy, OnInit, ViewChild, Input, OnChanges, SimpleChanges } from '@angular/core';
import { DataTableDirective } from 'angular-datatables';
import { Subject } from 'rxjs';
import { UserService } from '../../../user/services/user.service';
import { ApiCallService } from '../../../services/api-call.service';
import { map } from 'rxjs/operators';
import { HttpHeaders } from '@angular/common/http';
import { DatePipe } from '@angular/common';

@Component({
  selector: 'cmdb-table',
  templateUrl: './table.component.html',
  styleUrls: ['./table.component.scss'],
  providers: [DatePipe]
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
   * Create advanced fields and only display if extended fields exist
   */
  @Input() summaries: any[] = [];

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
    className: 'btn btn-success btn-sm mr-1',
    attr: {
      'data-toggle': 'modal',
      'data-target': '#insertModal'
    }
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

  constructor(private userService: UserService, private apiCallService: ApiCallService, private datePipe: DatePipe) {
  }

  ngOnInit() {
    this.buildTable();
  }

  ngOnChanges(changes: SimpleChanges): void {
    this.rerender();
    this.buildTable();
    this.dtTrigger.next();
  }

  private buildAdvancedDtOptions() {
    if (this.summaries !== undefined
      && this.summaries.length > 0
      && this.extendedFields !== undefined
      && this.extendedFields.length > 0) {
      const colVis = {
        extend: 'collection',
        className: 'btn btn-info btn-sm mr-1 dropdown-toggle',
        text: '<i class="fa fa-cog" aria-hidden="true"></i>',
        collectionLayout: 'dropdown-menu overflow-auto',
        buttons: function() {
          const columnButton = [];
          // tslint:disable-next-line:prefer-for-of
          for (let i = 0; i < this.extendedFields.length; i++) {
            {
              columnButton.push(
                {
                  text: this.extendedFields[i].label,
                  extend: 'columnToggle',
                  columns: '.toggle-' + this.extendedFields[i].name,
                  className: 'dropdown-item ' + this.extendedFields[i].name,
                });
            }
          }
          columnButton.push({
            extend: 'colvisRestore',
            text: 'Restore',
            className: 'btn btn-secondary btn-lg btn-block',
            action: function() {
              this.rerender();
              this.dtTrigger.next();
            }.bind(this)
          });
          return columnButton;
        }.bind(this),
      };

      // create optional Options
      const visTargets: any[] = [0, 1, 2 , 3, -3, -2, -1];
      for (let i = 0; i < this.summaries.length; i++) {
        visTargets.push(i + 4);
      }

      this.dtOptions.columnDefs = [
        { orderable: false, targets: 'nosort' },
        { visible: true, targets: visTargets },
        { visible: false, targets: '_all' }
      ];
      this.dtOptions.order = [[2, 'asc']];
      this.dtButtons.push(colVis);
    }
  }

  private buildButtons() {
    this.dtButtons.length = 0;
    this.dtButtons.push(this.add);
    this.dtButtons.push(this.print);
  }

  private buildOptions(buttons) {
    this.dtOptions = {};
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
    this.buildAdvancedDtOptions();
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
        console.log(data);
      });
    }
  }

  public delObject(value: any) {
    const id = value.public_id;
    this.apiCallService.callDeleteRoute('object/' + id).subscribe(data => {
      console.log(data);
    });
  }

  public export(fileExtension: string) {

    const httpHeader =  new HttpHeaders({
        'Content-Type': 'application/' + fileExtension
      });

    this.apiCallService.callExportRoute('export/' + fileExtension + '/' + this.linkRoute + 'type/' + 1, httpHeader)
      .pipe(
        map(res => {
          const timestamp = this.datePipe.transform(new Date(), 'MM_dd_yyyy_hh_mm_ss');
          return {
            filename: timestamp + '.' + fileExtension,
            data: res
          };
        })
      ).subscribe(res => {
        const blob = new Blob([res.data], {type: 'application/xml'});
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');

        document.body.appendChild(a);
        a.setAttribute('style', 'display: none');
        a.href = url;
        a.download = res.filename;
        a.click();
        window.URL.revokeObjectURL(url);
        a.remove(); // remove the element
      }, error => {
        console.log('download error:', JSON.stringify(error));
      }, () => {
        console.log('Completed file download.');
      });
  }
}
