/*
* dataGerry - OpenSource Enterprise CMDB
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

import { Component, OnDestroy, OnInit, ViewChild } from '@angular/core';
import { ApiCallService } from '../../../services/api-call.service';
import { DataTableDirective } from 'angular-datatables';
import { Subject } from 'rxjs';

@Component({
  selector: 'cmdb-newest-view',
  templateUrl: './newest-view.component.html',
  styleUrls: ['./newest-view.component.scss']
})
export class NewestViewComponent implements OnInit, OnDestroy {

  @ViewChild(DataTableDirective)
  public dtElement: DataTableDirective;
  public dtTrigger: Subject<any> = new Subject();
  public dtOptions: DataTables.Settings = {};

  public newest: [];

  readonly url = 'object/newest/';

  constructor(private api: ApiCallService) { }

  ngOnInit() {
    this.dtOptions = {
      ordering: true,
      order: [[1, 'asc']],
      language: {
        search: '',
        searchPlaceholder: 'Filter...'
      },
    };

    this.callObjects();
  }

  private callObjects() {
    this.api.callGetRoute(this.url).subscribe( data => {
      this.newest = data as [];
      this.rerender();
      this.dtTrigger.next();
    });
  }

  ngOnDestroy(): void {
    // Do not forget to unsubscribe the event
    this.dtTrigger.unsubscribe();
  }

  public rerender(): void {
    if (typeof this.dtElement.dtInstance !== 'undefined') {
      this.dtElement.dtInstance.then((dtInstance: DataTables.Api) => {
        // Destroy the table first
        dtInstance.destroy();
      });
    }
  }

  public delObject(id: number) {
    this.api.callDeleteRoute('object/' + id).subscribe(data => {
      this.callObjects();
    });
  }

}
