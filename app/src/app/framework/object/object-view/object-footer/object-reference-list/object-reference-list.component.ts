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

import { Component, Input, OnDestroy, ViewChild } from '@angular/core';
import { Subject } from 'rxjs';
import { RenderResult } from '../../../../models/cmdb-render';
import { ObjectService } from '../../../../services/object.service';
import { DataTableDirective } from 'angular-datatables';

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

  public constructor(private objectService: ObjectService) {
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

  public ngOnDestroy(): void {
    this.dtTrigger.unsubscribe();
  }
}
