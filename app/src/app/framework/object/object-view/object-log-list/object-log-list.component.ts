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

import { Component, Input, OnChanges, OnDestroy, OnInit, SimpleChanges, ViewChild } from '@angular/core';
import { LogService } from '../../../services/log.service';
import { CmdbLog } from '../../../models/cmdb-log';
import { Subject } from 'rxjs';
import { DataTableDirective } from 'angular-datatables';

@Component({
  selector: 'cmdb-object-log-list',
  templateUrl: './object-log-list.component.html',
  styleUrls: ['./object-log-list.component.scss']
})
export class ObjectLogListComponent implements OnInit, OnChanges, OnDestroy {

  private id: number;
  @ViewChild(DataTableDirective, {static: true})
  private dtElement: DataTableDirective;
  public dtOptions: any = {};
  public dtTrigger: Subject<any> = new Subject();

  @Input()
  set publicID(publicID: number) {
    this.id = publicID;
    if (this.id !== undefined && this.id !== null) {
      this.loadLogList();
    }
  }

  get publicID(): number {
    return this.id;
  }

  public logList: CmdbLog[] = [];

  constructor(private logService: LogService) {
  }

  private loadLogList() {
    this.logService.getLogsByObject(this.publicID).subscribe((logs: CmdbLog[]) => {
      this.logList = logs;
    }, (error) => {
      console.log(error);
    }, () => {
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

  public ngOnInit(): void {
    this.dtOptions = {
      ordering: true,
      order: [1, 'desc'],
      language: {
        search: '',
        searchPlaceholder: 'Filter...'
      }
    };
  }

  public ngOnChanges(changes: SimpleChanges): void {
  }

  public ngOnDestroy(): void {
    this.dtTrigger.unsubscribe();
  }

}
