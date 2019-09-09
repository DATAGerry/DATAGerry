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

import { AfterContentInit, Component, EventEmitter, Input, OnDestroy, OnInit, Output, ViewChild } from '@angular/core';
import { CmdbLog } from '../../../../framework/models/cmdb-log';
import { DataTableDirective } from 'angular-datatables';
import { Subject } from 'rxjs';

@Component({
  selector: 'cmdb-activate-tab',
  templateUrl: './activate-tab.component.html',
  styleUrls: ['./activate-tab.component.scss']
})
export class ActivateTabComponent implements AfterContentInit, OnDestroy, OnInit {

  @ViewChild(DataTableDirective, {static: true})
  dtElement: DataTableDirective;
  dtTrigger: Subject<any> = new Subject();
  dtOptions: DataTables.Settings = {};

  // tslint:disable-next-line:variable-name
  private _activeLogList: CmdbLog[];

  @Input('activeLogList')
  public set activeLogList(logList: CmdbLog[]) {
    this._activeLogList = logList;
    this.dtTrigger.next();
  }

  public get activeLogList() {
    return this._activeLogList;
  }
  @Output() deleteEmitter = new EventEmitter<number>();

  public constructor() {
  }

  public ngOnInit(): void {
    this.dtOptions = {
      retrieve: true,
      ordering: true,
      order: [0, 'desc'],
      language: {
        search: '',
        searchPlaceholder: 'Filter...'
      }
    };
  }

  public ngOnDestroy(): void {
    this.dtTrigger.unsubscribe();
  }

  public ngAfterContentInit(): void {
    this.dtTrigger.next();
  }

  public rerender() {
    this.dtElement.dtInstance.then((dtInstance: DataTables.Api) => {
      dtInstance.destroy();
    });
  }

}
