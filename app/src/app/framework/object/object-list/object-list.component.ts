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
  private records: number;

  readonly dtButtons: any[] = [];
  public summaries: any[] = [];
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
    // tslint:disable-next-line:only-arrow-functions
    this.router.routeReuseStrategy.shouldReuseRoute = function() {
      return false;
    };
  }

  private getMetaData(id) {
    this.masterSelected = false;
    this.pageTitle = 'Object List';
    this.hasSummaries = false;
    if (typeof id !== 'undefined') {
      this.typeID = id;
      this.hasSummaries = true;
      this.typeService.getType(id).subscribe((data: CmdbType) => {
        this.typeInstance = data;
        this.faIcon = data.render_meta.icon;
        this.pageTitle = data.label + ' list';
      });
      this.objService.countObjectsByType(this.typeID).subscribe(totals => {
        this.records = totals;
        this.hasSummaries = totals > 0;
      });
    } else {
      this.objService.countObjects().subscribe(totals => this.records = totals);
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
        const startx =  dataTablesParameters[START];
        const lengthx = dataTablesParameters[LENGTH];

        if (dataTablesParameters[SEARCH].value !== null
          && dataTablesParameters[SEARCH].value !== ''
          && dataTablesParameters[SEARCH].value !== undefined) {
          that.objService.getObjects(that.typeID, startx, lengthx).subscribe(resp => {
            that.objectLists = resp;
            if (resp.length > 0) {
              that.summaries = resp[0].summaries;
              that.selectedObjects.length = 0;
              that.masterSelected = false;
            }
            callback({
              data: [],
              recordsTotal: that.records,
              recordsFiltered: that.records
            });
          });
        } else {
          that.objService.getObjects(that.typeID, startx, lengthx).subscribe(resp => {
            that.objectLists = resp;
            if (resp.length > 0) {
              that.summaries = resp[0].summaries;
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
      },
      columnDefs: [
        { className: 'dt-head-center', width: '1%', targets: 0 },
        { className: 'dt-head-center', width: '5%', targets: [1, 2] },
        { className: 'dt-head-center', width: '8%', targets: [-1, -2, -3, 3 ]},
      ],
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

//  LOGIC

  /*
    Build table increments
   */
  private buildDtTable() {
    this.buildDefaultDtOptions();
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

  /*
    Table action events
   */
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
