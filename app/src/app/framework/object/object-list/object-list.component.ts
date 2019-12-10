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


import {AfterViewInit, Component, OnDestroy, OnInit, ViewChild} from '@angular/core';
import { ApiCallService } from '../../../services/api-call.service';
import { ActivatedRoute, Router } from '@angular/router';
import { NgxSpinnerService } from 'ngx-spinner';
import { ObjectService } from '../../services/object.service';
import { DataTableDirective } from 'angular-datatables';
import { Subject } from 'rxjs';
import { map } from 'rxjs/operators';
import { CmdbMode } from '../../modes.enum';
import { FileSaverService } from 'ngx-filesaver';
import { DatePipe } from '@angular/common';
import { CmdbType } from '../../models/cmdb-type';
import { TypeService } from '../../services/type.service';
import { RenderResult } from '../../models/cmdb-render';
import { FileService } from '../../../export/export.service';

@Component({
  selector: 'cmdb-object-list',
  templateUrl: './object-list.component.html',
  styleUrls: ['./object-list.component.scss'],
})
export class ObjectListComponent implements AfterViewInit, OnDestroy, OnInit {

  @ViewChild(DataTableDirective, {static: false})
  public dtElement: DataTableDirective;
  public dtOptions: any = {}; // : DataTables.Settings = {};
  public dtTrigger: Subject<any> = new Subject();

  private url: string ;
  private records: number;

  readonly dtButtons: any[] = [];
  public summaries: any[] = [];
  public columnFields: any[] = [];
  public items: any[] = [];

  public pageTitle: string = 'List';
  public faIcon: string;
  public objectLists: RenderResult[];
  public hasSummaries: boolean = false;
  public formatList: any[] = [];
  public selectedObjects: string[] = [];
  public typeID: number = null;
  public mode: CmdbMode = CmdbMode.Simple;

  constructor(private apiCallService: ApiCallService, private objService: ObjectService,
              private fileService: FileService, private route: ActivatedRoute, private router: Router,
              private spinner: NgxSpinnerService, private fileSaverService: FileSaverService,
              private datePipe: DatePipe, private typeService: TypeService) {
    this.fileService.callFileFormatRoute().subscribe(data => {
      this.formatList = data;
    });
  }

  private getMetaData(id) {
    this.url = 'object/';
    this.pageTitle = 'Object List';
    this.hasSummaries = false;
    if (typeof id !== 'undefined') {
      this.url = this.url + 'type/' + id;
      this.typeID = id;
      this.hasSummaries = true;
      this.typeService.getType(id).subscribe((data: CmdbType) => {
        this.faIcon = data.render_meta.icon;
        this.pageTitle = data.label + ' list';
      });
      this.objService.countObjectsByType(this.typeID).subscribe(count => this.records = count);
    } else {
      this.objService.countObjects().subscribe(count => this.records = count);
    }
  }

  ngOnInit(): void {
    this.route.params.subscribe((id) => {
      this.getMetaData(id.publicID);
      this.getObjects();
    });
  }

  public getObjects() {
    const that = this;
    const START = 'start';
    const LENGTH = 'length';
    const SEARCH = 'search';
    this.rerender();
    this.dtOptions = {
      pagingType: 'full_numbers',
      serverSide: true,
      processing: true,
      ajax: (dataTablesParameters: RenderResult[], callback) => {
        const param = {
          start: dataTablesParameters[START],
          length: dataTablesParameters[LENGTH],
        };
        if (this.typeID != null) {
          const type = 'type';
          param[type] = that.typeID;
        }

        if (dataTablesParameters[SEARCH].value !== null
          && dataTablesParameters[SEARCH].value !== ''
          && dataTablesParameters[SEARCH].value !== undefined) {
          const was = 'object/filter/' + dataTablesParameters[SEARCH].value;
          that.apiCallService.callGetRoute( was, {params: param}).subscribe(resp => {
            that.objectLists = resp;
            that.summaries = resp !== null ? resp[0].summaries : [];
            that.selectedObjects.length = 0;
            callback({
              data: [],
              recordsTotal: that.records,
              recordsFiltered: that.records,
            });
          });
        } else {
          that.apiCallService.callGetRoute(this.url, {params: param}).subscribe(resp => {
            that.objectLists = resp;
            that.summaries = resp !== null ? resp[0].summaries : [];
            that.selectedObjects.length = 0;
            callback({
              data: [],
              recordsTotal: that.records,
              recordsFiltered: that.records,
            });
          });
        }
      },
      columnDefs: [ {
        orderable: false,
        targets:   0
      } ],
      language: {
        search: '',
        searchPlaceholder: 'Filter...'
      }
    };
  }

  ngAfterViewInit(): void {
    this.dtTrigger.next();
  }

  ngOnDestroy(): void {
    // Do not forget to unsubscribe the event
    this.dtTrigger.unsubscribe();

    // If a table is initialized while it is hidden,
    // the browser calculates the width of the columns
    this.dtElement.dtInstance.then((dtInstance: any) => {
      dtInstance.columns.adjust()
        .responsive.recalc();
    });
  }

  rerender(): void {
    if (typeof this.dtElement !== 'undefined' && typeof this.dtElement.dtInstance !== 'undefined') {
      this.dtElement.dtInstance.then((dtInstance: DataTables.Api) => {
        // Destroy the table first
        dtInstance.destroy();
        // Call the dtTrigger to rerender again
        this.dtTrigger.next();
      });
    }
  }

//  LOGIC

  /*
    Build table increments
   */

  private buildDtTable() {
    this.buildAdvancedButtons();
    this.buildAdvancedDtOptions();
  }

  private buildAdvancedButtons() {
    if (this.hasSummaries) {
      this.dtButtons.push(
        {
          extend: 'collection',
          className: 'btn btn-secondary btn-sm mr-1 dropdown-toggle',
          text: '<i class="fas fa-cog"></i>',
          collectionLayout: 'dropdown-menu overflow-auto',
          buttons: function() {
            const columnButton = [];
            // tslint:disable-next-line:prefer-for-of
            if (this.columnFields == null) {
              this.columnFields = [];
            }
            let i = 0;
            for (const obj of this.columnFields) {
              {
                columnButton.push(
                  {
                    text: this.columnFields[i].label,
                    extend: 'columnToggle',
                    columns: '.toggle-' + this.columnFields[i].name,
                    className: 'dropdown-item ' + this.columnFields[i].name,
                  });
              }
              i++;
            }
            columnButton.push({
              extend: 'colvisRestore',
              text: 'Restore',
              className: 'btn btn-secondary btn-sm btn-block',
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
    const table = $('#object-list-datatable').DataTable();
    const buttons = this.dtButtons;
    this.dtOptions = {
      ordering: true,
      order: [[2, 'asc']],
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
    if (this.hasSummaries && this.summaries != null) {
      const visTargets: any[] = [0, 1, 2, 3, -3, -2, -1];
      for (const summary of this.summaries) {
        visTargets.push(this.columnFields.findIndex(i => i.name === summary.name) + 4);
      }
      this.dtOptions.columnDefs = [
        { visible: true, targets: visTargets },
        { visible: false, targets: '_all' },
        { orderable: false, className: 'select-checkbox', targets:   0 },
      ];
      this.dtOptions.order = [[2, 'asc']];
      this.dtOptions.ordering = true;
    }
  }

  /*
    Table action events
   */

  public addColumn() {
    const table: any = $('#object-list-datatable');
    const dataTable: any = table.DataTable();
    const columns: any = dataTable.columns();
    console.log(columns.data());
  }

  public selectAll() {
    const table: any = $('#object-list-datatable');
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

  public updateDisplay(publicID: any): void {
    const index = this.selectedObjects.findIndex(d => d === publicID); // find index in your array
    if (index > -1) {
      this.selectedObjects.splice(index, 1); // remove element from array
    } else {
      this.selectedObjects.push(publicID);
    }
  }

  public delObject(value: any) {
    const modalComponent = this.objService.openModalComponent(
      'Delete Object',
      'Are you sure you want to delete this Object?',
      'Cancel',
      'Delete');

    modalComponent.result.then((result) => {
      if (result) {
        const id = value.object_information.object_id;
        this.apiCallService.callDeleteRoute('object/' + id).subscribe(data => {
          this.route.params.subscribe((typeId) => {
            this.getObjects();
          });
        });
      }
    });
  }

  public delManyObjects() {
    if (this.selectedObjects.length > 0) {
      const modalComponent = this.objService.openModalComponent(
        'Delete selected Objects',
        'Are you sure, you want to delete all selected objects?',
        'Cancel',
        'Delete');

      modalComponent.result.then((result) => {
        if (result) {
          if (this.selectedObjects.length > 0) {
            this.apiCallService.callDeleteManyRoute('object/delete/' + this.selectedObjects.toString()).subscribe(data => {
              this.route.params.subscribe((id) => {
                this.getObjects();
              });
            });
          }
        }
      });
    }
  }

  public exportingFiles(exportType: any) {
    if (this.selectedObjects.length === 0 || this.selectedObjects.length === this.items.length) {
      this.fileService.getObjectFileByType(this.objectLists[0].type_information.type_id, exportType.id)
        .subscribe(res => this.downLoadFile(res, exportType));
    } else {
      this.fileService.callExportRoute('/file/object/' + this.selectedObjects.toString(), exportType.id)
        .subscribe(res => this.downLoadFile(res, exportType));
    }
  }

  public downLoadFile(data: any, exportType: any) {
    const timestamp = this.datePipe.transform(new Date(), 'MM_dd_yyyy_hh_mm_ss');
    this.fileSaverService.save(data.body, timestamp + '.' + exportType.label);
  }
}
