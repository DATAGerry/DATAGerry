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

import {AfterContentInit, Component, EventEmitter, Input, OnDestroy, OnInit, Output, ViewChild} from '@angular/core';
import { DataTableDirective } from 'angular-datatables';
import { Subject } from 'rxjs';
import { ExportdLog } from '../../../models/exportd-log';

@Component({
  selector: 'cmdb-exportdjob-activate-tab',
  templateUrl: './activate-exportd-tab.component.html',
  styleUrls: ['./activate-exportd-tab.component.scss']
})
export class ActivateExportdTabComponent implements AfterContentInit, OnDestroy, OnInit {

  @ViewChild(DataTableDirective)
  public dtElement: DataTableDirective;
  public dtOptions: any = {};
  public dtTrigger: Subject<any> = new Subject();

  // tslint:disable-next-line:variable-name
  private _activeLogList: ExportdLog[];

  @Input('activeLogList')
  public set activeLogList(logList: ExportdLog[]) {
    this._activeLogList = logList;
    this.dtTrigger.next();
  }

  public get activeLogList() {
    return this._activeLogList;
  }

  @Output() deleteEmitter = new EventEmitter<number>();

  constructor() { }

  ngOnInit() {
    this.dtOptions = {
      ordering: true,
      order: [[1, 'desc']],
      dom:
        '<"row" <"col-sm-2" l> <"col-sm-3" B > <"col" f> >' +
        '<"row" <"col-sm-12"tr>>' +
        '<\"row\" <\"col-sm-12 col-md-5\"i> <\"col-sm-12 col-md-7\"p> >',
      buttons: [],
      orderFixed: [2, 'desc'],
      rowGroup: {
        enable: true,
        endRender(rows) {
          return `Number of logs in this action: ${ rows.count() }`;
        },
        dataSrc: 2
      },
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
