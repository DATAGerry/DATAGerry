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


import {AfterViewInit, Component, ElementRef, OnDestroy, OnInit, ViewChild} from '@angular/core';
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
  @ViewChild('dtTableElement', {static: false}) dtTableElement: ElementRef;

  private url: string ;
  private records: number;

  readonly dtButtons: any[] = [];
  public summaries: any[] = [];
  public columnFields: any[] = [];
  public items: any[] = [];

  public columns: any[] = [];

  public masterSelected: boolean = false;

  public pageTitle: string = 'List';
  public faIcon: string;
  public objectLists: RenderResult[];
  public hasSummaries: boolean = false;
  public formatList: any[] = [];
  public selectedObjects: string[] = [];
  public typeID: number = null;
  public typeInstance: CmdbType = undefined;
  public mode: CmdbMode = CmdbMode.Simple;

  constructor(private apiCallService: ApiCallService, private objService: ObjectService,
              private fileService: FileService, private route: ActivatedRoute, private router: Router,
              private spinner: NgxSpinnerService, private fileSaverService: FileSaverService,
              private datePipe: DatePipe, private typeService: TypeService) {
    this.fileService.callFileFormatRoute().subscribe(data => {
      this.formatList = data;
    });
    this.router.routeReuseStrategy.shouldReuseRoute = function () {
      return false;
    };
  }

  private getMetaData(id) {
    this.url = 'object/';
    this.masterSelected = false;
    this.pageTitle = 'Object List';
    this.hasSummaries = false;
    if (typeof id !== 'undefined') {
      this.url = this.url + 'type/' + id;
      this.typeID = id;
      this.hasSummaries = true;
      this.typeService.getType(id).subscribe((data: CmdbType) => {
        this.typeInstance = data;
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
      this.buildDtTable();
    });
  }

  public getObjects() {
    const that = this;
    const START = 'start';
    const LENGTH = 'length';
    const SEARCH = 'search';
    const FIELDS = 'fields';
    this.reload();
    this.dtOptions = {
      // <"col-sm-3" B >
      dom: '<"row" <"col-sm-3" l>  <"col" f> >' +
        '<"row" <"col-sm-12"tr>>' +
        '<\"row\" <\"col-sm-12 col-md-5\"i> <\"col-sm-12 col-md-7\"p> >',
      pagingType: 'full_numbers',
      serverSide: true,
      processing: true,
      ordering: false,
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
            that.objectLists = resp === null ? [] : resp;
            if (resp != null) {
              that.objectLists = resp !== null ? resp : [];
              that.summaries = resp !== null ? resp[0].summaries : [];
              that.selectedObjects.length = 0;
              that.masterSelected = false;
            }
            callback({
              data: [],
              recordsTotal: that.objectLists.length,
              recordsFiltered: that.objectLists.length,
            });
          });
        } else {
          that.apiCallService.callGetRoute(this.url, {params: param}).subscribe(resp => {
            that.objectLists = resp === null ? [] : resp;
            if (resp != null) {
              that.objectLists = resp !== null ? resp : [];
              that.summaries = resp !== null ? resp[0].summaries : [];
              that.selectedObjects.length = 0;
              that.masterSelected = false;
            }
            callback({
              data: [],
              recordsTotal: that.records,
              recordsFiltered: that.records,
            });
          });
        }
      },
      language: {
        search: '',
        searchPlaceholder: 'Filter...'
      }
    };
  }

  ngAfterViewInit(): void {
    this.dtTrigger.next();
  }

  public getMergeNameToLabel(value: string) {
    return this.summaries.find(x => x.name === value);
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

  reload(): void {
    if (typeof this.dtElement !== 'undefined' && typeof this.dtElement.dtInstance !== 'undefined') {
      this.dtElement.dtInstance.then((dtInstance: DataTables.Api) => {
        // Destroy the table first
        dtInstance.destroy();
        // Call the dtTrigger to rerender again
        this.dtTrigger.next();
      });
    }
  }

  async rerender(newSettings?: DataTables.Settings) {
    try {
      await this.dtElement.dtInstance.then((dtInstance: DataTables.Api) => {
        if (newSettings) {
          // FIX To ensure that the DT doesn't break when we don't get columns
          if (this.dtOptions.columns !== undefined) {
            // console.log('ASDFASfd')
            // this.buildDtTable();
          }
          console.log('ASDFASfd')
          this.buildDtTable();
          if (newSettings.columns && newSettings.columns.length > 1) {
            dtInstance.destroy();
            this.dtOptions = Promise.resolve(newSettings);
            this.displayTable(this.dtTableElement);
          }
        }
      });
    } catch (error) {
      console.log(`DT Rerender Exception: ${error}`);
    }
    return Promise.resolve(null);
  }

  private displayTable(renderIn: ElementRef): void {
    this.dtElement.dtInstance = new Promise((resolve, reject) => {
      Promise.resolve(this.dtOptions).then(dtOptions => {
        // Using setTimeout as a "hack" to be "part" of NgZone
        setTimeout(() => {
          $(renderIn.nativeElement).empty();
          const dt = $(renderIn.nativeElement).DataTable(dtOptions);
          resolve(dt);
        });
      }).catch(error => reject(error));
    });
  }

//  LOGIC

  /*
    Build table increments
   */

  private buildDtTable() {
    // this.buildDefaultDtButtons();
    // this.buildAdvancedButtons();
    this.buildDefaultDtOptions();
    // this.buildAdvancedDtOptions();
  }

  private buildDefaultDtButtons() {
    this.dtButtons.length = 0;
    this.dtButtons.push(
      {
        // add new
        text: '<i class="fas fa-plus"></i> Add',
        className: 'btn btn-success btn-sm mr-1',
        action: function() {
          if (this.typeID === null) {
            this.router.navigate(['/framework/object/add']);
          } else {
            this.router.navigate(['/framework/object/add/' + this.typeID]);
          }

        }.bind(this)
      }
    );
  }

  private buildAdvancedButtons() {
    if (this.hasSummaries) {
      const that = this;
      this.dtButtons.push(
        {
          extend: 'collection',
          className: 'btn btn-secondary btn-sm mr-1 dropdown-toggle',
          text: '<i class="fas fa-cog"></i>',
          collectionLayout: 'dropdown-menu overflow-auto',
          buttons: function() {
            const columnButton = [];
            // tslint:disable-next-line:prefer-for-of
            if (that.typeInstance.fields == null) {
              that.typeInstance.fields = [];
            }
            let i = 0;
            for (const obj of that.typeInstance.fields) {
              {
                columnButton.push(
                  {
                    text: that.typeInstance.fields[i].label,
                    extend: 'columnToggle',
                    columns: '.toggle-' + that.typeInstance.fields[i].name,
                    className: 'dropdown-item ' + that.typeInstance.fields[i].name,
                  });
              }
              i++;
            }
            columnButton.push({
              extend: 'colvisRestore',
              text: 'Restore',
              className: 'btn btn-secondary btn-sm btn-block',
              action: function() {
                that.reload();
              }
            });
            return columnButton;
          }
        },
      );
    }
  }

  private buildDefaultDtOptions() {
    const buttons = this.dtButtons;
    this.dtOptions.order = [[2, 'asc']];
    this.dtOptions.select = {
      style:    'multi',
      selector: 'td:first-child'
    };
    this.dtOptions.language = {
      search: '',
      searchPlaceholder: 'Filter...'
    };
    this.dtOptions.dom =
      '<"row" <"col-sm-3" l> <"col-sm-3" B > <"col" f> >' +
      '<"row" <"col-sm-12"tr>>' +
      '<\"row\" <\"col-sm-12 col-md-5\"i> <\"col-sm-12 col-md-7\"p> >';
    // Configure the buttons
    // Declare the use of the extension in the dom parameter
    this.dtOptions.buttons = {
      dom: {
        container: {
          className: 'dt-buttons btn-group btn-group-sm'
        }
      },
      buttons,
    };
  }

  private buildAdvancedDtOptions() {
    if (this.hasSummaries) {
      const visTargets: any[] = [0, 1, 2, 3, -3, -2, -1];
      this.typeService.getType(this.typeID).subscribe(data => {
        for (const summary of data.render_meta.summary.fields) {
          visTargets.push(data.fields.findIndex(i => i.name === summary.name) + 4);
        }
        this.dtOptions.columnDefs = [
          { visible: true, targets: visTargets },
          { visible: false, targets: '_all' },
          { orderable: false, className: 'select-checkbox', targets:   0 },
        ];
        this.dtOptions.order = [[2, 'asc']];
        this.dtOptions.ordering = true;
      });
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

  checkUncheckAll() {
    this.selectedObjects = [];
    const allCheckbox: any = document.getElementsByClassName('select-checkbox');

    for (const box of allCheckbox) {
      box.checked = this.masterSelected;
      this.selectedObjects.push(box.name);
    }
    if (!this.masterSelected) {
      this.selectedObjects = [];
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
