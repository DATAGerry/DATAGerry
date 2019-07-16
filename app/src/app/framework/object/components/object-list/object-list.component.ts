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


import {Component, OnDestroy, ViewChild} from '@angular/core';
import { ApiCallService } from '../../../../services/api-call.service';
import { ActivatedRoute } from '@angular/router';
import { NgxSpinnerService } from 'ngx-spinner';
import { DatePipe } from '@angular/common';
import { ObjectService } from '../../../services/object.service';
import { DataTableDirective } from 'angular-datatables';
import { Subject } from 'rxjs';
import {CmdbObject} from '../../../models/cmdb-object';
import {map} from 'rxjs/operators';
import {HttpHeaders} from '@angular/common/http';
import {ExportService} from '../../../../services/export.service';

@Component({
  selector: 'cmdb-object-list',
  templateUrl: './object-list.component.html',
  styleUrls: ['./object-list.component.scss'],
  providers: [DatePipe]
})
export class ObjectListComponent implements OnDestroy {

  @ViewChild(DataTableDirective, {static: false})
  public dtElement: DataTableDirective;
  public dtOptions: any = {}; // : DataTables.Settings = {};
  public dtTrigger: Subject<any> = new Subject();
  readonly dtButtons: any[] = [];

  private summaries: [];
  private columnFields: [];
  private items: [] ;
  public pageTitle: string = 'List';
  public objectLists: {};
  public hasSummaries: boolean = false;
  readonly $date: string = '$date';

  constructor(private apiCallService: ApiCallService, private objService: ObjectService,
              private exportService: ExportService, private route: ActivatedRoute,
              private spinner: NgxSpinnerService, private datePipe: DatePipe) {
    this.route.params.subscribe((id) => {
      this.init(id);
    });
  }

  private init(id) {
    this.getRouteObjects(id.publicID);
  }

  private getRouteObjects(id) {
    let url = 'object/';
    this.pageTitle = 'Object List';
    this.hasSummaries = false;
    if ( typeof id !== 'undefined') {
      url = url + 'type/' + id;
      this.hasSummaries = true;
    }

    this.apiCallService.callGetRoute(url)
      .pipe(
        map( dataArray => {
          const lenx = dataArray.length;
          this.summaries = lenx > 0 ? dataArray[0].summaries : [];
          this.columnFields = lenx > 0 ? dataArray[0].fields : [];
          this.items = lenx > 0 ? dataArray : [];

          if (this.hasSummaries && lenx > 0) {
            this.pageTitle = dataArray[0].label + ' List';
          }

          return[ {items: this.items, columnFields: this.columnFields} ];
        })
      )
      .subscribe(
        data => {
          this.spinner.show();
          this.buildDtTable();

          setTimeout( () => {
            this.objectLists = data;
            this.rerender();
            this.dtTrigger.next();
            this.spinner.hide();
          }, 100);
        });

  }

  /*
    Build table increments
   */

  private buildDtTable() {
    this.buildDefaultDtButtons();
    this.buildAdvancedButtons();
    this.buildDefaultDtOptions();
    this.buildAdvancedDtOptions();
  }

  private buildDefaultDtButtons() {
    this.dtButtons.length = 0;
    this.dtButtons.push(
      {
        // add new
        text: '<i class="fa fa-plus" aria-hidden="true"></i> Add',
        className: 'btn btn-success btn-sm mr-1',
        attr: {
          'data-toggle': 'modal',
          'data-target': '#insertModal'
        }
      }
    );

    this.dtButtons.push(
      {
        // print
        text: 'Print <i class="fa fa-print" aria-hidden="true"></i>',
        extend: 'print',
        className: 'btn btn-info btn-sm mr-1'
      }
    );
  }

  private buildAdvancedButtons() {
    if (this.hasSummaries) {
      this.dtButtons.push(
        {
          extend: 'collection',
          className: 'btn btn-secondary btn-sm mr-1 dropdown-toggle',
          text: '<i class="fa fa-cog" aria-hidden="true"></i>',
          collectionLayout: 'dropdown-menu overflow-auto',
          buttons: function() {
            const columnButton = [];
            // tslint:disable-next-line:prefer-for-of
            for (let i = 0; i < this.columnFields.length; i++) {
              {
                columnButton.push(
                  {
                  text: this.columnFields[i].label,
                  extend: 'columnToggle',
                  columns: '.toggle-' + this.columnFields[i].name,
                  className: 'dropdown-item ' + this.columnFields[i].name,
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
        },
      );
    }
  }

  private buildDefaultDtOptions() {
    const buttons = this.dtButtons;
    this.dtOptions = {
      ordering: true,
      order: [[5, 'asc']],
      columnDefs: [ {
        targets: 'nosort',
        orderable: false,
      } ],
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

  private buildAdvancedDtOptions() {
    if (this.hasSummaries) {
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
    }
  }

  public ngOnDestroy(): void {
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

  /*
    Table action events
   */

  public checkType(value) {
    if (value != null && value.hasOwnProperty('$date')) {
      return '<span>' + this.datePipe.transform(value[this.$date], 'dd/mm/yyyy - hh:mm:ss') + '</span>';
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

  public delObject(value: any) {
    const id = value.public_id;
    this.apiCallService.callDeleteRoute('object/' + id).subscribe(data => {
      this.route.params.subscribe((typeId) => {
        this.init(typeId);
      });
    });
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
      this.apiCallService.callDeleteManyRoute('object/delete/' + publicIds ).subscribe(data => {
        this.route.params.subscribe((id) => {
          this.init(id);
        });
      });
    }
  }

  public update(instance: any) {

    const updateInstance = new CmdbObject();
    updateInstance.public_id = Number(instance.public_id);
    updateInstance.type_id = instance.type_id;
    updateInstance.version = '1.0.0';
    updateInstance.creation_time = instance.creation_time;
    updateInstance.author_id = instance.author_id;
    updateInstance.active = instance.active;

    const fieldsList: any[] = [];
    for (const field of instance.fields) {
      const text: any = document.getElementsByName(field.name)[0];
      fieldsList.push({name: field.name, value: text.value });
    }

    updateInstance.fields = fieldsList;
    this.objService.postUpdateObject(updateInstance).subscribe(res => {
      console.log(res);
    });
  }

  public export(fileExtension: string) {

    const httpHeader =  new HttpHeaders({
      'Content-Type': 'application/' + fileExtension
    });

    this.exportService.callExportRoute('export/' + fileExtension + '/' + 'object/type/' + 1, httpHeader)
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
