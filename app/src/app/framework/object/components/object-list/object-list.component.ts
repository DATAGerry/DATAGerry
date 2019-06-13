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


import { Component, OnDestroy, ViewChild } from '@angular/core';
import { DataTableDirective } from 'angular-datatables';
import { Subject } from 'rxjs';
import { ApiCallService } from '../../../../services/api-call.service';
import { ActivatedRoute } from '@angular/router';
import { NgxSpinnerService } from 'ngx-spinner';
import { map } from 'rxjs/operators';
import { DatePipe } from '@angular/common';
import { element } from 'protractor';
import {getClassName} from "codelyzer/util/utils";

@Component({
  selector: 'cmdb-object-list',
  templateUrl: './object-list.component.html',
  styleUrls: ['./object-list.component.scss'],
  providers: [DatePipe]
})
export class ObjectListComponent implements OnDestroy {

  @ViewChild(DataTableDirective)
  public dtElement: DataTableDirective;
  public dtOptions: any = {}; // : DataTables.Settings = {};
  public dtTrigger: Subject<any> = new Subject();

  private summaries: [];
  private columnFields: [];
  private items: [];
  public objectLists: {};
  public isCategorized: boolean = false;
  readonly $date: string = '$date';

  constructor(private apiCallService: ApiCallService, private route: ActivatedRoute,
              private spinner: NgxSpinnerService, private dateFormatPipe: DatePipe) {

    this.route.params.subscribe((id) => {
      this.init(id);
    });
  }

  private init(id) {
    this.getRouteObjects(id.publicID);
  }

  private buildDtOptions() {
    let buttons = [];

    buttons.push(
      {
        // add new
        text: '<i class="fa fa-file-o" aria-hidden="true"></i>',
        className: 'btn btn-light',
        action: function (e, dt, node, config) {
          console.log('New');
        }
      }
    );

    buttons.push(
      {
        // edit
        text: '<i class="fa fa-pencil-square-o" aria-hidden="true"></i>',
        className: 'btn btn-light',
        action: function (e, dt, node, config) {
          console.log('Edit');
        }
      }
    );

    buttons.push(
      {
        // delete
        text: '<i class="fa fa-trash-o" aria-hidden="true"></i>',
        className: 'btn btn-light',
        action: function () {
          const allCheckbox: any = document.getElementsByClassName('select-checkbox');
          for (const box of allCheckbox) {
            if (box.checked) {
              console.log('Delete');
            }
          }
        }.bind(this)
      }
    );

    buttons.push(
      {
        // copy
        text: '<i class="fa fa-files-o" aria-hidden="true"></i>',
        extend: 'copy',
        className: 'btn btn-light'
      }
    );

    buttons.push(
      {
        // print
        text: '<i class="fa fa-print" aria-hidden="true"></i>',
        extend: 'print',
        className: 'btn btn-light'
      }
    );

    buttons.push(
      {
        // export to exel
        text: '<i class="fa fa-file-excel-o" aria-hidden="true"></i>',
        extend: 'excel',
        className: 'btn btn-light'
      }
    );

    if(this.isCategorized) {
      buttons.push(
        {
          extend: 'collection',
          className: 'btn btn-light dropdown-toggle',
          text: '<i class="fa fa-cog" aria-hidden="true"></i>',
          collectionLayout: 'dropdown-menu overflow-auto',
          buttons: function ( e, dt, node, config ) {
            const columnButton = [];
            for(let i = 0; i<this.columnFields.length; i++){
              {
                columnButton.push(
                  {
                  text: this.columnFields[i].label,
                  extend: 'columnToggle',
                  columns: '.toggle-'+this.columnFields[i].name,
                  className: 'dropdown-item '+ this.columnFields[i].name,
                })
              }
            }
            columnButton.push({
                  extend: 'colvisRestore',
                  text: 'Restore',
                  className: 'btn btn-secondary btn-lg btn-block'
                });
            return columnButton;
          }.bind(this),
        },
      );
    }

    this.dtOptions = {
      ordering: true,
      order: [[1, 'asc']],
      retrieve: true,
      language: {
        search: '',
        searchPlaceholder: 'Filter...'
      },dom:
        "<'row' <'col-sm-3' l> <'col-sm-3' B > <'col' f> >" +
        "<'row' <'col-sm-12'tr>>" +
        "<'row' <'col-sm-12 col-md-5'i> <'col-sm-12 col-md-7'p> >",
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

    if(this.isCategorized) {
      let visTargets: any[] = [0,1,2,3,-1];
      for (let i = 0; i<this.summaries.length; i++) {
        visTargets.push(i+4);
      }
      this.dtOptions['columnDefs'] = [
        { visible: true, targets: visTargets },
        { targets: '_all', visible: false }
      ]
    }
  }

  private getRouteObjects(id) {
    let url = 'object/';
    if ( typeof id !== 'undefined') {
      url = url + 'type/' + id;
      this.isCategorized = true;
    }

    this.apiCallService.callGetRoute(url)
      .pipe(
        map( dataArray => {
          this.summaries = dataArray[0].summaries;
          this.columnFields = dataArray[0].obj_fields;
          this.items = dataArray;
          return[ {items: this.items, columnFields: this.columnFields} ];
        })
      )
      .subscribe(
      data => {

        this.spinner.show();
        this.buildDtOptions();

        setTimeout( () => {
          this.objectLists = data;
          this.rerender();
          this.dtTrigger.next();
          this.spinner.hide();
        }, 100);
      });

  }

  ngOnDestroy(): void {
    // Do not forget to unsubscribe the event
    this.dtTrigger.unsubscribe();
  }

  public rerender(): void {
    if (typeof this.dtElement.dtInstance !== 'undefined') {
      this.dtElement.dtInstance.then((dtInstance: DataTables.Api) => {
        // Destroy the table first
        dtInstance.destroy();
      });
    }
  }

  public checkType(value) {
    if (value.hasOwnProperty('$date')) {
      return '<span>' + this.dateFormatPipe.transform(value[this.$date], 'dd/mm/yyyy - hh:mm:ss') + '</span>';
    }
    return '<span>' + value + '</span>';
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

  public delObject(id: number) {
    this.apiCallService.callDeleteRoute('object/' + id).subscribe(data => {
    });
  }
}
