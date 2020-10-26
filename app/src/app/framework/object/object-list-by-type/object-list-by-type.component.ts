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


import {
  AfterViewInit,
  Component,
  ElementRef,
  HostListener,
  OnDestroy,
  OnInit,
  Renderer2,
  ViewChild
} from '@angular/core';
import { DataTableDirective } from 'angular-datatables';
import { Subject } from 'rxjs';
import { ObjectService } from '../../services/object.service';
import { RenderResult } from '../../models/cmdb-render';
import { DatePipe } from '@angular/common';
import { ActivatedRoute, ActivatedRouteSnapshot, Router } from '@angular/router';
import { FileService } from '../../../export/export.service';
import { FileSaverService } from 'ngx-filesaver';
import { DataTableFilter, DataTablesResult } from '../../models/cmdb-datatable';
import { TypeService } from '../../services/type.service';
import { CmdbType } from '../../models/cmdb-type';
import { PermissionService } from '../../../auth/services/permission.service';
import { ObjectPreviewModalComponent } from '../modals/object-preview-modal/object-preview-modal.component';
import { NgbModal, NgbModalRef } from '@ng-bootstrap/ng-bootstrap';
import { UserSetting } from '../../../management/user-settings/models/user-setting';
import { UserSettingsDBService } from '../../../management/user-settings/services/user-settings-db.service';
import { AuthService } from '../../../auth/services/auth.service';

import {
  ObjectTableUserPayload,
  ObjectTableUserSettingConfig
} from '../../../management/user-settings/models/settings/object-table-user-setting';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { SidebarService } from '../../../layout/services/sidebar.service';

@Component({
  selector: 'cmdb-object-list-by-type',
  templateUrl: './object-list-by-type.component.html',
  styleUrls: ['./object-list-by-type.component.scss'],
  providers: [DatePipe]
})
export class ObjectListByTypeComponent implements AfterViewInit, OnInit, OnDestroy {

  @ViewChild('dtTableElement', { static: false }) dtTableElement: ElementRef;
  @ViewChild(DataTableDirective, { static: false })
  public dtElement: DataTableDirective;
  public dtOptions: any = {};
  public dtTrigger: Subject<any> = new Subject();
  public objects: DataTablesResult;

  private modalRef: NgbModalRef;

  // Header
  public pageTitle: string = 'List';
  public faIcon: string;

  // Header Buttons
  public typeID;
  public formatList: any[] = [];

  // Select properties
  public selectedObjects: string[] = [];

  /**
   * Component wide un-subscriber.
   */
  private subscriber: Subject<void> = new Subject<void>();

  /**
   * User settings for this route.
   */
  public tableUserSetting: UserSetting<ObjectTableUserPayload>;

  /**
   * Selector if the config is new.
   */

  public currentTableSettingsConfig: ObjectTableUserSettingConfig;

  public stateSelected: boolean = false;

  /**
   * FormGroup for settings label
   */
  public settingForm: FormGroup;

  /**
   * Current type from the route resolve.
   */
  public type: CmdbType;

  constructor(private objectService: ObjectService, private typeService: TypeService, private datePipe: DatePipe,
              private fileSaverService: FileSaverService, private fileService: FileService,
              private router: Router, private route: ActivatedRoute, private renderer2: Renderer2,
              private permissionService: PermissionService, private modalService: NgbModal,
              private userSettingsDB: UserSettingsDBService, private authService: AuthService,
              private sidebarService: SidebarService) {

    this.router.routeReuseStrategy.shouldReuseRoute = (future: ActivatedRouteSnapshot, curr: ActivatedRouteSnapshot) => {
      return false;
    };

    this.fileService.callFileFormatRoute().subscribe(data => {
      this.formatList = data;
    });

    this.type = this.route.snapshot.data.type as CmdbType;
    this.tableUserSetting = this.route.snapshot.data.userSetting as UserSetting<ObjectTableUserPayload>;
    if (!this.tableUserSetting) {
      this.tableUserSetting = new UserSetting<ObjectTableUserPayload>(
        this.router.url.toString().substring(1).split('/').join('-'),
        this.authService.currentUserValue.public_id,
        new ObjectTableUserPayload([])
      );
      this.userSettingsDB.addSetting(this.tableUserSetting);
    }
    this.settingForm = new FormGroup({
      label: new FormControl('', Validators.required)
    });

  }

  public ngOnInit() {

    this.route.params.subscribe((params) => {
      this.typeID = this.type.public_id;
      this.faIcon = this.type.render_meta.icon;
      this.pageTitle = this.type.label + ' list';
      this.dtOptionbuilder(this.typeID);
    });
  }

  private dtOptionbuilder(typeID: number) {
    this.dtOptions = {
      stateSave: true,
      stateSaveCallback: (settings, data) => {
        console.log('Save');
        this.currentTableSettingsConfig = {
          data,
          active: true,
        } as ObjectTableUserSettingConfig;
        this.saveConfig();
      },
      stateLoadCallback: (settings, callback) => {
        console.log('Load');
        try {
          for (const config of this.tableUserSetting.payload.tableConfigs) {
            if (config.active) {
              this.currentTableSettingsConfig = config.data;
              return config.data;
            }
          }
        } catch (e) {
          return callback(null);
        }
        return callback(null);
      },
      pagingType: 'full_numbers',
      pageLength: 25,
      lengthMenu: [10, 25, 50, 100, 250, 500],
      order: [[2, 'asc']],
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
          this.objectService.getObjectsByFilter(typeID, filter).subscribe((resp: any) => {
            this.selectedObjects.length = 0;
            this.objects = resp;
            // Render columns afterwards
            this.rerender(this.dtOptions).then();

            callback({
              data: this.objects.data,
              recordsTotal: this.objects.recordsTotal,
              recordsFiltered: this.objects.recordsFiltered,
            });
          });
        } else {
          this.objectService.getObjects().subscribe((resp: any) => {
            this.selectedObjects.length = 0;
            this.objects = resp;
            // Render columns afterwards
            this.rerender(this.dtOptions).then();

            callback({
              data: this.objects.data,
              recordsTotal: this.objects.recordsTotal,
              recordsFiltered: this.objects.recordsFiltered,
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

            postfixButtons: [{
              extend: 'colvisRestore',
              text: 'Restore',
              tag: 'button',
              className: 'btn btn-secondary btn-sm btn-block mt-2 mb-2',
            }]
          }
        ]
      },
      rowCallback: (row: Node, data: RenderResult) => {
        const self = this;
        $('td:first-child', row).off('click');
        $('td:first-child', row).on('click', () => {
          self.updateDisplay(data.object_information.object_id.toString());
        });
        return row;
      },
      select: {
        style: 'multi',
        selector: 'td:first-child'
      },
      columns: [
        {
          data: null, defaultContent: '',
          title: '<input type="checkbox" class="select-all-objects" name="select-all-objects">',
          className: 'select-checkbox text-center', sortable: false, orderable: false
        },
        {
          data: 'object_information.active', title: 'Active', name: 'active',
          render(data) {
            if (data) {
              return '<span class="badge badge-success"> A </span>';
            }
            return '<span class="badge badge-danger"> D </span>';
          }
        },
        { data: 'object_information.object_id', title: 'ID', name: 'public_id' }
      ]
    };
  }

  @HostListener('document:click', ['$event'])
  dtActionClick(event: any): void {
    if ((event.target as Element).className.indexOf('preview-object-action') > -1) {
      this.previewObject(parseInt((event.target as Element).id, 10));
    } else if ((event.target as Element).className.indexOf('view-object-action') > -1) {
      this.router.navigate(['/framework/object/type/view/', (event.target as Element).id]);
    } else if ((event.target as Element).className.indexOf('copy-object-action') > -1) {
      this.router.navigate(['/framework/object/copy/', (event.target as Element).id]);
    } else if ((event.target as Element).className.indexOf('edit-object-action') > -1) {
      this.router.navigate(['/framework/object/edit/', (event.target as Element).id]);
    } else if ((event.target as Element).className.indexOf('delete-object-action') > -1) {
      this.delObject(parseInt((event.target as Element).id, 10));
    }
  }

  public ngAfterViewInit(): void {
    this.renderer2.listen('document', 'click', (event) => {
      const actionClassList = (event.target as Element).classList;
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

  public ngOnDestroy(): void {
    this.dtTrigger.unsubscribe();
    this.subscriber.next();
    this.subscriber.complete();

    if (this.modalRef) {
      this.modalRef.close();
    }
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
      console.log(`DT Rerender Exception: ${ error }`);
    }
    return Promise.resolve(null);
  }

  private buildDtColumns(newSettings: DataTables.Settings) {
    const that = this;
    for (let i = 0; i < this.objects.data[0].fields.length; i++) {
      newSettings.columns.push(
        {
          data: 'fields.' + i + '.value',
          title: that.objects.data[0].fields[i].label,
          name: that.objects.data[0].fields[i].name,
        });
    }
    newSettings.columns.push(
      { data: 'object_information.author_name', title: 'Author', name: 'author_id' },
      {
        data: 'object_information.creation_time', title: 'Creation Time', name: 'creation_time',
        render(data) {
          return that.datePipe.transform(data.$date, 'dd/MM/yyyy - HH:mm:ss');
        }
      },
      {
        data: null,
        title: 'Action',
        className: 'td-button-actions text-center',
        orderable: false,
        render(data) {
          const rights: string[] = that.permissionService.currentUserRights.map(right => right.name);
          const baseRights = rights.includes('base.*')
            || rights.includes('base.system.*')
            || rights.includes('base.framework.*')
            || rights.includes('base.framework.object.*');
          let view = '';
          let copy = '';
          let edit = '';
          let del = '';
          let preview = '';

          if (rights.includes('base.framework.object.view') || baseRights) {
            view = '<span id="' + data.object_information.object_id + '' +
              '" class="far fa-eye mr-1 view-object-action" title="view"></span>';

            preview = '<span id="' + data.object_information.object_id + '' +
              '" class="far fa-file-powerpoint mr-1 preview-object-action" title="preview"></span>';
          }
          if (rights.includes('base.framework.object.add') || baseRights) {
            copy = '<span id="' + data.object_information.object_id + '' +
              '" class="far fa-clone mr-1 copy-object-action" title="copy"></span>';
          }
          if (rights.includes('base.framework.object.edit') || baseRights) {
            edit = '<span id="' + data.object_information.object_id + '' +
              '" class="far fa-edit mr-1 edit-object-action" title="edit"></span>';
          }
          if (rights.includes('base.framework.object.delete') || baseRights) {
            del = '<span id="' + data.object_information.object_id + '' +
              '" class="far fa-trash-alt mr-1 delete-object-action" title="delete"></span>';
          }

          return view + copy + edit + preview + del;
        }
      }
    );
    newSettings.columnDefs = [
      { className: 'text-center', width: '20px', targets: 0, orderable: false },
      { className: 'text-center', width: '5%', targets: [1, 2] },
      { className: 'text-center', width: '8%', targets: [-1, -2, -3, 3] },
    ];
  }

  private buildAdvancedDtOptions() {
    const summaries = this.objects.data[0].summaries;
    if (summaries != null) {
      const visTargets: any[] = [0, 1, 2, -3, -2, -1];
      for (const summary of summaries) {
        visTargets.push(this.objects.data[0].fields.findIndex(i => i.name === summary.name) + 3);
      }
      this.dtOptions.columnDefs = [
        { orderable: false, targets: 'nosort' },
        { visible: true, targets: visTargets },
        { visible: false, targets: '_all' }
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
        this.objectService.deleteObject(publicID).subscribe(() => {
          this.ajaxReload();
          this.sidebarService.updateTypeCounter(this.typeID);
        });
      }
    });
  }

  private previewObject(publicID: number) {
    this.objectService.getObject(publicID).subscribe(resp => {
      this.modalRef = this.modalService.open(ObjectPreviewModalComponent, { size: 'lg' });
      this.modalRef.componentInstance.renderResult = resp;
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
            this.objectService.deleteManyObjects(this.selectedObjects.toString()).subscribe(() => {
              this.ajaxReload();
              this.sidebarService.updateTypeCounter(this.typeID);
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
      this.fileService.callExportRoute(this.selectedObjects.toString(), exportType.id)
        .subscribe(res => this.downLoadFile(res, exportType));
    }
  }

  public downLoadFile(data: any, exportType: any) {
    const timestamp = this.datePipe.transform(new Date(), 'MM_dd_yyyy_hh_mm_ss');
    this.fileSaverService.save(data.body, timestamp + '.' + exportType.label);
  }

  /**
   * Save Config
   */
  public saveConfig(label: string = ''): void {
    this.tableUserSetting.payload.tableConfigs.forEach(c => {
      c.active = false;
    });

    this.currentTableSettingsConfig.label = label;
    const configIDX = this.tableUserSetting.payload.tableConfigs.findIndex(c => c.label && c.label === label);
    if (configIDX > -1) {
      this.tableUserSetting.payload.tableConfigs[configIDX] = this.currentTableSettingsConfig;
    } else {
      this.tableUserSetting.payload.tableConfigs.push(this.currentTableSettingsConfig);
    }

    this.userSettingsDB.updateSetting(this.tableUserSetting);
  }


  /**
   * Toggle between multiple setting states.
   * @param selected ObjectTableUserSettingConfig
   */
  public selectConfig(selected: ObjectTableUserSettingConfig): void {
    for (const config of this.tableUserSetting.payload.tableConfigs) {
      config.active = config === selected;
    }
    this.userSettingsDB.updateSetting(this.tableUserSetting);
    this.currentTableSettingsConfig = selected;
    this.dtElement.dtInstance.then((dtInstance: DataTables.Api) => {
      dtInstance.destroy();
      this.displayTable(this.dtTableElement);
    });
  }

  /**
   * Set all settings activation status to false.
   * Same as reset default setting.
   */
  public default(): void {
    if (this.tableUserSetting) {
      for (const config of this.tableUserSetting.payload.tableConfigs) {
        config.active = false;
      }
      this.userSettingsDB.updateSetting(this.tableUserSetting);
    }
    this.currentTableSettingsConfig = undefined;
    this.dtElement.dtInstance.then((dtInstance: DataTables.Api) => {
      dtInstance.destroy();
      this.displayTable(this.dtTableElement);
    });
  }

  /**
   * Delete a config from the setting.
   * @param selected The form setting
   */
  public deleteConfig(selected: ObjectTableUserSettingConfig): void {
    const index = this.tableUserSetting.payload.tableConfigs.indexOf(selected, 0);
    if (index > -1) {
      this.tableUserSetting.payload.tableConfigs.splice(index, 1);
    }
    this.userSettingsDB.updateSetting(this.tableUserSetting);
  }


  /**
   * Get the label control of the settings.
   */
  public get settingLabel(): FormControl {
    return this.settingForm.get('label') as FormControl;
  }

}
