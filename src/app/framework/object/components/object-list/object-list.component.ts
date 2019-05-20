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


import { AfterViewInit, Component, OnDestroy, OnInit, ViewChild } from '@angular/core';
import { DataTableDirective } from 'angular-datatables';
import { Subject } from 'rxjs';
import { ApiCallService } from "../../../../services/api-call.service";

@Component({
  selector: 'cmdb-object-list',
  templateUrl: './object-list.component.html',
  styleUrls: ['./object-list.component.scss']
})
export class ObjectListComponent implements AfterViewInit, OnDestroy, OnInit {

  @ViewChild(DataTableDirective)
  public dtElement: DataTableDirective;

  dtOptions: DataTables.Settings = {};
  object_lists = [];

  // Use this trigger because fetching the list of objects can be quite long,
  // this ensure the data is fetched before rendering
  public dtTrigger: Subject<any> = new Subject();

  constructor(private apiCallService: ApiCallService,) { }

  ngOnInit() {
    this.dtOptions = {
      ordering: true,
      order: [[1, 'asc']],
      language: {
        search: '',
        searchPlaceholder: 'Filter...'
      },
    };

    this.apiCallService.callGetRoute("object/").subscribe(
      data => {
        this.object_lists = data as [];
        this.dtTrigger.next();
      });
  }

  ngAfterViewInit(): void {


  }

  ngOnDestroy(): void {
    // Do not forget to unsubscribe the event
    this.dtTrigger.unsubscribe();
  }

}
