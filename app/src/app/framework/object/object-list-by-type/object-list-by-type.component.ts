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


import { AfterViewInit, Component, ComponentFactoryResolver, ElementRef, OnDestroy, OnInit, Renderer2, ViewChild} from '@angular/core';
import { DataTableDirective } from 'angular-datatables';
import { Subject } from 'rxjs';
import { ObjectService } from '../../services/object.service';
import { RenderResult } from '../../models/cmdb-render';
import { DatePipe } from '@angular/common';
import { ActivatedRoute, Router } from '@angular/router';
import { FileService } from '../../../export/export.service';
import { FileSaverService } from 'ngx-filesaver';
import { DataTableFilter, DataTablesResult } from '../../models/cmdb-datatable';
import { TypeService } from '../../services/type.service';
import { CmdbType } from '../../models/cmdb-type';

@Component({
  selector: 'cmdb-object-list-by-type',
  templateUrl: './object-list-by-type.component.html',
  styleUrls: ['./object-list-by-type.component.scss'],
  providers: [DatePipe]
})
export class ObjectListByTypeComponent implements AfterViewInit, OnInit, OnDestroy {

  @ViewChild('dtTableElement', {static: false}) dtTableElement: ElementRef;
  @ViewChild(DataTableDirective, {static: false})
  public dtElement: DataTableDirective;
  public dtOptions: any = {};
  public dtTrigger: Subject<any> = new Subject();
  public objects: DataTablesResult;

  // Header
  public pageTitle: string = 'List';
  public faIcon: string;

  // Header Buttons
  public typeID;
  public formatList: any[] = [];

  // Select properties
  public selectedObjects: string[] = [];

  constructor(private objectService: ObjectService, private typeService: TypeService, private datePipe: DatePipe,
              private fileSaverService: FileSaverService, private fileService: FileService,
              private router: Router, private route: ActivatedRoute, private renderer: Renderer2) {
    this.fileService.callFileFormatRoute().subscribe(data => {
      this.formatList = data;
    });
    // tslint:disable-next-line:only-arrow-functions
    this.router.routeReuseStrategy.shouldReuseRoute = function() {
      return false;
    };
  }

  ngOnInit() {
    this.route.params.subscribe((params) => {
      this.typeID = params.publicID;
      this.typeService.getType(this.typeID).subscribe((tInstance: CmdbType) => {
        this.faIcon = tInstance.render_meta.icon;
        this.pageTitle = tInstance.label + ' list';
      });
      this.dtOptionbuilder(params.publicID);
    });
  }

  private dtOptionbuilder(typeID: number) {
    const that = this;
    this.dtOptions = {
      pagingType: 'full_numbers',
      order: [[ 2, 'asc' ]],
      dom:
        '<"row" <"col-sm-3" l> <"col-sm-3" B > <"col" f> >' +
        '<"row" <"col-sm-12"tr>>' +
        '<\"row\" <\"col-sm-12 col-md-5\"i> <\"col-sm-12 col-md-7\"p> >',
      serverSide: true,
      processing: true,
      ajax: (dtParams: any, callback) => {
        const filter: DataTableFilter = new DataTableFilter();
        filter.start = dtParams.start;
        filter.length = dtParams.length;
        filter.orderBy = dtParams.columns[dtParams.order[0].column].name;
        filter.direction = dtParams.order[0].dir;
        filter.search = dtParams.search.value;

        if (filter.search !== null
          && filter.search !== ''
          && filter.search !== undefined) {
          that.objectService.getObjectsByFilter(typeID, filter).subscribe((resp: any) => {
            that.selectedObjects.length = 0;
            that.objects = resp;
            // Render columns afterwards
            this.rerender(this.dtOptions);

            callback({
              data: that.objects.data,
              recordsTotal: that.objects.recordsTotal,
              recordsFiltered: that.objects.recordsFiltered,
            });
          });
        } else {
          that.objectService.getObjects(typeID, filter).subscribe((resp: any) => {
            that.selectedObjects.length = 0;
            that.objects = resp;
            // Render columns afterwards
            this.rerender(this.dtOptions);

            callback({
              data: that.objects.data,
              recordsTotal: that.objects.recordsTotal,
              recordsFiltered: that.objects.recordsFiltered,
            });
          });
        }
      },
      buttons: {
        dom: {
          button: {
            tag: 'span'
          }
        },
        buttons: [
          {
            extend: 'colvis',
            columns: ':not(":first,:last")',
            className: 'btn btn-secondary btn-sm mr-1 dropdown-toggle',
            collectionLayout: 'dropdown-menu overflow-auto',
            text: '<i class="fas fa-cog"></i>',

            postfixButtons: [ {
              extend: 'colvisRestore',
              text: 'Restore',
              tag: 'button',
              className: 'btn btn-secondary btn-sm btn-block mt-2 mb-2',
            } ]
          }
        ]
      },
      rowCallback: (row: Node, data: RenderResult) => {
        const self = this;
        $('td:first-child', row).unbind('click');
        $('td:first-child', row).bind('click', () => {
          self.updateDisplay(data.object_information.object_id.toString());
        });
        return row;
      },
      select: {
        style:    'multi',
        selector: 'td:first-child'
      },
      columns: [
        { data: null, defaultContent: '',
          title: '<input type="checkbox" class="select-all-objects" name="select-all-objects">',
          className: 'select-checkbox text-center', sortable: false, orderable: false },
        {
          data: 'object_information.active', title: 'Active', name: 'active',
          render(data) {
            if (data) {
              return '<span class="badge badge-success"> A </span>';
            }
            return '<span class="badge badge-danger"> D </span>';
          }
        },
        {data: 'object_information.object_id', title: 'ID', name: 'public_id'}
      ]
    };
  }

  ngAfterViewInit(): void {
    this.renderer.listen('document', 'click', (event) => {
      const actionClassList = (event.target as Element).classList;
      if (actionClassList.contains('delete-object')) {
        this.delObject(parseInt((event.target as Element).id, 10));
      }

      if (actionClassList.contains('select-all-objects')) {
        const dataTable: any = $('#dt-object-list').DataTable();
        const rows: any = dataTable.rows();
        this.selectedObjects = [];
        if ($('.select-all-objects').is(':checked')) {
          rows.select();
          let lenx: number = rows.data().length - 1;
          while (lenx >= 0) {
            this.selectedObjects.push(rows.data()[lenx].object_information.object_id.toString());
            lenx--;
          }
        } else {
          rows.deselect();
        }
      }
    });
  }

  ngOnDestroy(): void {
    this.dtTrigger.unsubscribe();
  }

  async rerender(newSettings?: DataTables.Settings) {
    try {
      await this.dtElement.dtInstance.then((dtInstance: DataTables.Api) => {

        // All-Checkbox set unchecked
        const selectAllObjects: any = $('.select-all-objects');
        if (selectAllObjects.is(':checked')) {
          selectAllObjects[0].checked = false;
        }
        // Render additional columns
        if (newSettings) {
          if (newSettings.columns) {
            // Render additional columns
            this.buildDtColumns(newSettings);
            this.buildAdvancedDtOptions();
          }
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

  private buildDtColumns(newSettings: DataTables.Settings) {
    const that = this;
    for (let i = 0; i < this.objects.data[0].fields.length; i++) {
      newSettings.columns.push(
        { data: 'fields.' + i + '.value',
          title: that.objects.data[0].fields[i].label,
          name: that.objects.data[0].fields[i].name,
        });
    }
    newSettings.columns.push(
      {data: 'object_information.author_name', title: 'Author', name: 'author_id'},
      {data: 'object_information.creation_time', title: 'Creation Time', name: 'creation_time',
        render(data) {
          return that.datePipe.transform(data.$date, 'dd/MM/yyyy - h:mm:ss');
        }
      },
      {
        data: null,
        title: 'Action',
        className: 'text-dark text-center',
        orderable: false,
        render(data) {
          const view = '<a class="text-dark mr-1" href="/framework/object/type/view/'
            + data.object_information.object_id + '"><i class="far fa-eye"></i></a>';
          const edit = '<a class="text-dark mr-1" href="/framework/object/edit/'
            + data.object_information.object_id + '"><i class="far fa-edit"></i></a>';
          const del = '<span id="' + data.object_information.object_id
            + '" class="far fa-trash-alt mr-1 delete-object"></span>';
          return view + edit + del;
        }
      }
    );
    newSettings.columnDefs = [
      { className: 'text-center', width: '20px', targets: 0, orderable: false },
      { className: 'text-center', width: '5%', targets: [1, 2] },
      { className: 'text-center', width: '8%', targets: [-1, -2, -3, 3 ]},
    ];
  }

  private buildAdvancedDtOptions() {
    const summaries = this.objects.data[0].summaries;
    const that = this;
    if (summaries != null) {
      const visTargets: any[] = [0, 1, 2, -3, -2, -1];
      for (const summary of summaries) {
        visTargets.push(this.objects.data[0].fields.findIndex(i => i.name === summary.name) + 3);
      }
      this.dtOptions.columnDefs = [
        {orderable: false, targets: 'nosort'},
        {visible: true, targets: visTargets},
        {visible: false, targets: '_all'}
      ];
    }
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

  private ajaxReload(): void {
    this.dtElement.dtInstance.then((dtInstance: DataTables.Api) => {
      dtInstance.ajax.reload();
    });
  }

  public updateDisplay(publicID: any): void {
    const index = this.selectedObjects.findIndex(d => d === publicID); // find index in your array
    if (index > -1) {
      this.selectedObjects.splice(index, 1); // remove element from array
    } else {
      this.selectedObjects.push(publicID);
    }
  }

  public delObject(publicID: number) {
    const modalComponent = this.objectService.openModalComponent(
      'Delete Object',
      'Are you sure you want to delete this Object?',
      'Cancel',
      'Delete');

    modalComponent.result.then((result) => {
      if (result) {
        this.objectService.deleteObject(publicID).subscribe(data => {
          this.ajaxReload();
        });
      }
    });
  }

  public delManyObjects() {
    if (this.selectedObjects.length > 0) {
      const modalComponent = this.objectService.openModalComponent(
        'Delete selected Objects',
        'Are you sure, you want to delete all selected objects?',
        'Cancel',
        'Delete');

      modalComponent.result.then((result) => {
        if (result) {
          if (this.selectedObjects.length > 0) {
            this.objectService.deleteManyObjects(this.selectedObjects.toString()).subscribe(data => {
              this.ajaxReload();
            });
          }
        }
      });
    }
  }

  public exportingFiles(exportType: any) {
    if (this.selectedObjects.length === 0) {
      this.fileService.getObjectFileByType(this.objects.data[0].type_information.type_id, exportType.id)
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
