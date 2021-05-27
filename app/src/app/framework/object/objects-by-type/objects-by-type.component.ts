/*
* DATAGERRY - OpenSource Enterprise CMDB
* Copyright (C) 2019 - 2021 NETHINKS GmbH
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
* along with this program. If not, see <https://www.gnu.org/licenses/>.
*/

import {
  Component,
  OnDestroy,
  OnInit, TemplateRef, ViewChild,
} from '@angular/core';
import { BehaviorSubject, ReplaySubject } from 'rxjs';
import { CmdbType } from '../../models/cmdb-type';
import { ActivatedRoute, Data, Router } from '@angular/router';
import { takeUntil } from 'rxjs/operators';
import { RenderResult } from '../../models/cmdb-render';
import { TableComponent } from '../../../layout/table/table.component';
import { Column, Sort, SortDirection, TableState, TableStatePayload } from '../../../layout/table/table.types';
import { ObjectService } from '../../services/object.service';
import { CollectionParameters } from '../../../services/models/api-parameter';
import { APIGetMultiResponse } from '../../../services/models/api-response';
import { CmdbMode } from '../../modes.enum';
import { FileService } from '../../../export/export.service';
import { FileSaverService } from 'ngx-filesaver';
import { ToastService } from '../../../layout/toast/toast.service';
import { SidebarService } from '../../../layout/services/sidebar.service';
import { NgbModal, NgbModalRef } from '@ng-bootstrap/ng-bootstrap';
import { ObjectsDeleteModalComponent } from '../modals/objects-delete-modal/objects-delete-modal.component';
import { UserSetting } from '../../../management/user-settings/models/user-setting';
import { UserSettingsDBService } from '../../../management/user-settings/services/user-settings-db.service';
import {
  convertResourceURL,
  UserSettingsService
} from '../../../management/user-settings/services/user-settings.service';
import { SupportedExporterExtension } from '../../../export/export-objects/model/supported-exporter-extension';

@Component({
  selector: 'cmdb-objects-by-type',
  templateUrl: './objects-by-type.component.html',
  styleUrls: ['./objects-by-type.component.scss']
})
export class ObjectsByTypeComponent implements OnInit, OnDestroy {

  /**
   * HTML ID of the table.
   * Used for user settings and table-states
   */
  public readonly id: string = 'table-objects-type';

  /**
   * Table component.
   */
  @ViewChild(TableComponent) objectsTableComponent: TableComponent<RenderResult>;

  @ViewChild('activeTemplate', { static: true }) activeTemplate: TemplateRef<any>;
  @ViewChild('fieldTemplate', { static: true }) fieldTemplate: TemplateRef<any>;
  @ViewChild('dateTemplate', { static: true }) dateTemplate: TemplateRef<any>;
  @ViewChild('actionTemplate', { static: true }) actionTemplate: TemplateRef<any>;

  /**
   * Component un-subscriber.
   */
  private subscriber: ReplaySubject<void> = new ReplaySubject<void>();

  /**
   * Current render results
   */
  public results: Array<RenderResult> = [];

  /**
   * Selected objects
   */
  public selectedObjects: Array<RenderResult> = [];
  public selectedObjectsIDs: Array<number> = [];

  /**
   * Total number of results
   */
  public totalResults: number = 0;

  /**
   * Current type from the route resolve.
   */
  private typeSubject: BehaviorSubject<CmdbType> = new BehaviorSubject<CmdbType>(undefined);

  /**
   * Getter for the type definition from the typeSubject.
   */
  public get type(): CmdbType {
    return this.typeSubject.getValue() as CmdbType;
  }

  public tableStateSubject: BehaviorSubject<TableState> = new BehaviorSubject<TableState>(undefined);

  public tableStates: Array<TableState> = [];

  public get tableState(): TableState {
    return this.tableStateSubject.getValue() as TableState;
  }

  /**
   * Objects loading flag.
   */
  public loading: boolean = false;

  /**
   * Render mode for the render elements.
   */
  public mode: CmdbMode = CmdbMode.Simple;

  /**
   * Default sort filter.
   */
  public sort: Sort = { name: 'public_id', order: SortDirection.DESCENDING } as Sort;

  /**
   * Filter parameter from table search
   */
  public filter: string;

  public selectReset: Array<RenderResult> = [];

  public initialVisibleColumns: Array<string> = [];

  public columns: Array<Column>;

  public readonly initPage: number = 1;
  public page: number = this.initPage;

  private readonly initLimit: number = 25;
  public limit: number = this.initLimit;

  public formatList: any[] = [];

  private deleteManyModalRef: NgbModalRef;

  constructor(private router: Router, private route: ActivatedRoute, private objectService: ObjectService,
              private fileService: FileService, private fileSaverService: FileSaverService,
              private toastService: ToastService, private sidebarService: SidebarService,
              private modalService: NgbModal, private indexDB: UserSettingsDBService<UserSetting, TableStatePayload>,
              private userSettingsService: UserSettingsService<UserSetting, TableStatePayload>) {
    this.route.data.pipe(takeUntil(this.subscriber)).subscribe((data: Data) => {
      if (data.userSetting) {
        const userSettingPayloads = (data.userSetting as UserSetting<TableStatePayload>).payloads
          .find(payloads => payloads.id === this.id);
        this.tableStates = userSettingPayloads.tableStates;
        this.tableStateSubject.next(userSettingPayloads.currentState);
      } else {
        this.tableStates = [];
        this.tableStateSubject.next(undefined);

        const statePayload: TableStatePayload = new TableStatePayload(this.id, []);
        const resource: string = convertResourceURL(this.router.url.toString());
        const userSetting = userSettingsService.createUserSetting<TableStatePayload>(resource, [statePayload]);
        this.indexDB.addSetting(userSetting);
      }
      this.typeSubject.next(data.type as CmdbType);
    });
    this.fileService.callFileFormatRoute().subscribe(data => {
      this.formatList = data;
    });
  }

  public ngOnInit(): void {
    this.typeSubject.asObservable().pipe(takeUntil(this.subscriber)).subscribe((type: CmdbType) => {
      this.reload(type);
    });
  }

  /**
   * Reload the table
   * @param type
   */
  public reload(type: CmdbType): void {
    this.resetTable();
    this.setColumns(type);
    if (this.tableState) {
      this.page = this.tableState.page;
      this.limit = this.tableState.pageSize;
      this.sort = this.tableState.sort;
      for (const col of this.columns) {
        col.hidden = !this.tableState.visibleColumns.includes(col.name);
      }
    }
    this.loadObjects();
  }

  public resetTable() {
    this.page = this.initPage;
    this.limit = this.initLimit;
    this.filter = undefined;
    this.selectedObjects = [];
  }

  private setColumns(type: CmdbType): void {

    const fields = type.fields || [];
    const summaryFields = type.render_meta.summary.fields || [];

    const columns = [
      {
        display: 'Active',
        name: 'active',
        data: 'object_information.active',
        searchable: false,
        sortable: false,
        template: this.activeTemplate,
        cssClasses: ['text-center'],
        style: { width: '6rem' }
      },
      {
        display: 'Public ID',
        name: 'public_id',
        data: 'object_information.object_id',
        searchable: true,
        sortable: true
      }
    ] as Array<Column>;

    for (const field of fields) {
      columns.push({
        display: field.label,
        name: `fields.${ field.name }`,
        data: field.name,
        sortable: true,
        searchable: false,
        hidden: !summaryFields.includes(field.name),
        render(data: RenderResult, item: RenderResult, column: Column, index?: number) {
          const renderedField = item.fields.find(f => f.name === column.data);
          if (!renderedField) {
            return {};
          }
          return {
            field: renderedField,
            value: renderedField.value
          };
        },
        template: this.fieldTemplate
      } as Column);
    }

    columns.push({
      display: 'Author',
      name: 'author_id',
      data: 'object_information.author_name',
      sortable: true,
      searchable: false,
    } as Column);

    columns.push({
      display: 'Creation Time',
      name: 'creation_time',
      data: 'object_information.creation_time',
      sortable: true,
      searchable: false,
      template: this.dateTemplate,
    } as Column);
    columns.push({
      display: 'Modification Time',
      name: 'last_edit_time',
      data: 'object_information.last_edit_time',
      sortable: true,
      searchable: false,
      template: this.dateTemplate,
      render(data: any, item?: any, column?: Column, index?: number) {
        if (!data) {
          return 'No modifications so far.';
        }
        return data;
      }
    } as Column);

    columns.push({
      display: 'Actions',
      name: 'actions',
      sortable: false,
      searchable: false,
      fixed: true,
      template: this.actionTemplate,
      cssClasses: ['text-center'],
      style: { width: '6em' }
    } as unknown as Column);

    this.initialVisibleColumns = columns.filter(c => !c.hidden).map(c => c.name);
    this.columns = columns;
  }

  /**
   * Load objects from the backend.
   */
  public loadObjects() {
    this.loading = true;
    this.selectedObjects = [];
    this.selectedObjectsIDs = [];

    const searchableColumns = this.columns.filter(c => c.searchable);
    const filter = this.filterBuilder(searchableColumns);
    const params: CollectionParameters = {
      filter, limit: this.limit,
      sort: this.sort.name, order: this.sort.order, page: this.page
    };
    this.objectService.getObjects(params).pipe(takeUntil(this.subscriber))
      .subscribe((apiResponse: APIGetMultiResponse<RenderResult>) => {
        this.results = apiResponse.results as Array<RenderResult>;
        this.totalResults = apiResponse.total;
        this.loading = false;
      });
  }

  /**
   * DB Query / Filter Builder
   * Creates a database query using the passed parameters.
   *
   * @param columns {@link Array<Column>} are taken into account in the query.
   * @return query {@link: any[]}
   */
  private filterBuilder(columns: Array<Column>) {
    const query = [];
    query.push({
      $match: {
        type_id: this.type.public_id
      }
    });
    if (this.filter) {
      const or = [];
      for (const column of columns) {
        const regex: any = {};
        regex[column.name] = {
          $regex: String(this.filter),
          $options: 'ismx'
        };
        or.push(regex);
      }
      // Search into reference fields
      query.push(
        {
            $lookup: {
            from: 'framework.objects',
            localField: 'fields.value',
            foreignField: 'public_id',
            as: 'data'
          }
        });

      query.push({ $project: {
          _id: 1,
          public_id: 1,
          type_id: 1,
          active: 1,
          author_id: 1,
          creation_time: 1,
          last_edit_time: 1,
          fields: 1,
          simple: {
            $reduce: {
              input: '$data.fields',
              initialValue: [],
              in: { $setUnion: ['$$value', '$$this'] }
            }
          }
        } });

      query.push({
          $group: {
            _id: '$_id',
            public_id : { $first: '$public_id' },
            type_id: { $first: '$type_id' },
            active: { $first: '$active' },
            author_id: { $first: '$author_id' },
            creation_time: { $first: '$creation_time' },
            last_edit_time: { $first: '$last_edit_time' },
            fields : { $first: '$fields' },
            simple: { $first: '$simple' },
          }
        });

      query.push({ $project:
            {
              _id: '$_id',
              public_id: 1,
              type_id: 1,
              active: 1,
              author_id: 1,
              creation_time: 1,
              last_edit_time: 1,
              fields: 1,
              references : { $setUnion: ['$fields', '$simple'] },
            }
        }
      );
      // Search for creation_time
      query.push(
        { $addFields: {
            creationString: { $dateToString: { format: '%Y-%m-%dT%H:%M:%S.%LZ', date: '$creation_time' } }
          }},
      );
      // Search for last_edit_time
      query.push(
        { $addFields: {
            editString: { $dateToString: { format: '%Y-%m-%dT%H:%M:%S.%LZ', date: '$last_edit_time' } }
          }},
      );
      // Search date in field values
      query.push(
        { $addFields: {
            references: {
              $map: {
                input: '$references',
                as: 'new_fields',
                in: {
                  $cond: [
                    { $eq: [{ $type: '$$new_fields.value' }, 'date'] },
                    { name: '$$new_fields.name', value: {
                      $dateToString: { format: '%Y-%m-%dT%H:%M:%S.%LZ', date: '$$new_fields.value' } }
                    },
                    { name: '$$new_fields.name', value: '$$new_fields.value'}
                  ]
                }
              }
            }
          }
        },
      );
      // Nasty public id quick hack
      query.push({
        $addFields: {
          public_id: { $toString: '$public_id' }
        }
      });
      or.push({
        public_id: {
          $elemMatch: {
            value: {
              $regex: String(this.filter),
              $options: 'ism'
            }
          }
        }
      });
      // Date string search
      or.push( { creationString: { $regex: String(this.filter), $options: 'ims' } } );
      or.push( { editString: { $regex: String(this.filter), $options: 'ims' } } );
      // Search Fields
      or.push({
        references: {
          $elemMatch: {
            value: {
              $regex: String(this.filter),
              $options: 'ism'
            }
          }
        }
      });
      query.push({ $match: { $or: or } });
    }
    return query;
  }

  /**
   * On table page change.
   * Reload all objects.
   *
   * @param page
   */
  public onPageChange(page: number) {
    this.page = page;
    this.loadObjects();
  }

  /**
   * On table page size change.
   * Reload all objects.
   *
   * @param limit
   */
  public onPageSizeChange(limit: number): void {
    this.page = this.initPage;
    this.limit = limit;
    this.loadObjects();
  }

  /**
   * On table sort change.
   * Reload all objects.
   *
   * @param sort
   */
  public onSortChange(sort: Sort): void {
    this.sort = sort;
    this.loadObjects();
  }

  /**
   * On table search change.
   * Reload all objects.
   *
   * @param search
   */
  public onSearchChange(search: any): void {
    this.page = this.initPage;
    if (search) {
      this.filter = search;
    } else {
      this.filter = undefined;
    }
    this.loadObjects();
  }

  /**
   * On table selection change.
   * Map selected items by the object id
   *
   * @param selectedItems
   */
  public onSelectedChange(selectedItems: Array<RenderResult>): void {
    this.selectedObjects = selectedItems;
    this.selectedObjectsIDs = selectedItems.map(m => m.object_information.object_id);
  }

  /**
   * Select a state.
   *
   * @param state
   */
  public onStateSelect(state: TableState): void {
    this.tableStateSubject.next(state);
    this.page = this.tableState.page;
    this.limit = this.tableState.pageSize;
    this.sort = this.tableState.sort;
    for (const col of this.columns) {
      col.hidden = !this.tableState.visibleColumns.includes(col.name);
    }
    this.loadObjects();
  }

  public onStateReset(): void {
    this.tableStateSubject.next(undefined);
    this.reload(this.type);
  }

  public exportingFiles(see: SupportedExporterExtension) {
    const optional = {classname: see.extension, zip: false, metadata: undefined};
    const columns = this.columns.filter(c => !c.hidden && !c.fixed);
    const filter = this.filterBuilder(columns);

    const properties = [];
    const fields = [];
    for (const col of columns) {
      const {name} = (col as any);
      if (name && name.startsWith('fields.')) {
        fields.push(name.replace('fields.', ''));
      } else {
        properties.push(name);
      }
    }
    optional.metadata = {header: properties, columns: fields};

    const exportAPI: CollectionParameters = {filter, optional, order: this.sort.order, sort: this.sort.name};
    if (this.selectedObjectsIDs.length > 0) {
      exportAPI.filter = [{$match: {public_id: {$in: this.selectedObjectsIDs}}}, ...filter] ;
    }
    this.fileService.callExportRoute(exportAPI, see.view)
      .subscribe(res => {
        this.fileSaverService.save(res.body, new Date().toISOString() + '.' + see.label);
      });
  }

  public onObjectDelete(publicID: number) {
    this.objectService.deleteObject(publicID).pipe(takeUntil(this.subscriber)).subscribe(response => {
        this.toastService.success(`Object ${ publicID } was deleted successfully`);
        this.sidebarService.updateTypeCounter(this.type.public_id);
        this.loadObjects();
      },
      (error) => {
        this.toastService.error(`Error while deleting object ${ publicID } | Error: ${ error }`);
      });
  }

  public onManyObjectDeletes() {
    if (this.selectedObjects.length > 0) {
      this.deleteManyModalRef = this.modalService.open(ObjectsDeleteModalComponent, { size: 'lg' });
      this.deleteManyModalRef.result.then((response: string) => {
        if (response === 'delete') {
          this.objectService.deleteManyObjects(this.selectedObjectsIDs.toString())
            .pipe(takeUntil(this.subscriber)).subscribe(() => {
            this.toastService.success(`Deleted ${ this.selectedObjects.length } objects successfully`);
            this.sidebarService.updateTypeCounter(this.type.public_id);
            this.selectedObjects = [];
            this.objectsTableComponent.selectedItems = [];
            this.loadObjects();
          });
        }
      });
    }
  }


  public ngOnDestroy(): void {
    this.subscriber.next();
    this.subscriber.complete();
  }

}
