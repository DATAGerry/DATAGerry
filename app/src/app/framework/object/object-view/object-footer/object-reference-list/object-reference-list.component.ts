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

import { Component, Input, OnDestroy, ViewChild} from '@angular/core';
import { Subject } from 'rxjs';
import { RenderResult } from '../../../../models/cmdb-render';
import { ObjectService } from '../../../../services/object.service';
import { DataTableDirective } from 'angular-datatables';
import { FileService } from '../../../../../export/export.service';
import { DatePipe } from '@angular/common';
import { FileSaverService } from 'ngx-filesaver';
import { ExportObjectsFileExtension } from '../../../../../export/export-objects/model/export-objects-file-extension';

@Component({
  selector: 'cmdb-object-reference-list',
  templateUrl: './object-reference-list.component.html',
  styleUrls: ['./object-reference-list.component.scss']
})
export class ObjectReferenceListComponent implements OnDestroy {

  private id: number;

  @ViewChild(DataTableDirective, {static: true})
  private dtElement: DataTableDirective;
  public dtOptions: any = {};
  public dtTrigger: Subject<any> = new Subject();

  public referenceList: RenderResult[] = [];
  public formatList: ExportObjectsFileExtension[] = [];

  @Input()
  set publicID(publicID: number) {
    this.id = publicID;
    if (this.id !== undefined && this.id !== null) {
      this.loadObjectReferences();
    }
  }

  get publicID(): number {
    return this.id;
  }

  public constructor(private objectService: ObjectService, private datePipe: DatePipe,
                     private fileSaverService: FileSaverService, private fileService: FileService) {
    this.fileService.callFileFormatRoute().subscribe(data => {
      this.formatList = data;
    });
  }

  private loadObjectReferences() {
    this.objectService.getObjectReferences(this.publicID).subscribe((references: RenderResult[]) => {
        this.referenceList = references;
      },
      (error) => {
        console.error(error);
      },
      () => {
        this.renderTable();
      });
  }

  private renderTable(): void {
    if (this.dtElement.dtInstance === undefined) {
      this.dtTrigger.next();
    } else {
      this.dtElement.dtInstance.then((dtInstance: DataTables.Api) => {
        dtInstance.destroy();
        this.dtTrigger.next();
      });
    }

  }

  /**
   * Exports the referenceList as zip
   *
   * @param exportType the filetype to be zipped
   */
  public exportingFiles(exportType: ExportObjectsFileExtension) {
    if (this.referenceList.length !== 0) {
      const objectIDs: number[] = [];
      for (const el of this.referenceList) {
        objectIDs.push(el.object_information.object_id);
      }
      this.fileService.callExportRoute(objectIDs.toString(), exportType.extension, true)
        .subscribe(res => this.downLoadFile(res));
    }
  }

  /**
   * Downloads file
   * @param data the file data to be downloaded
   */
  public downLoadFile(data: any) {
    const timestamp = this.datePipe.transform(new Date(), 'MM_dd_yyyy_hh_mm_ss');
    this.fileSaverService.save(data.body, timestamp + '.' + 'zip');
  }

  public ngOnDestroy(): void {
    this.dtTrigger.unsubscribe();
  }
}
