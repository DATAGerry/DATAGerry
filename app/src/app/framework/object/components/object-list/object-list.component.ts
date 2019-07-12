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


import { Component } from '@angular/core';
import { ApiCallService } from '../../../../services/api-call.service';
import { ActivatedRoute } from '@angular/router';
import { NgxSpinnerService } from 'ngx-spinner';
import { DatePipe } from '@angular/common';
import { ObjectService } from '../../../services/object.service';

@Component({
  selector: 'cmdb-object-list',
  templateUrl: './object-list.component.html',
  styleUrls: ['./object-list.component.scss'],
  providers: [DatePipe]
})
export class ObjectListComponent {

  public pageTitle: string = 'Object list';
  public items: [] ;
  public hasSummaries: boolean = false;
  public currentRoutID: any;

  constructor(private apiCallService: ApiCallService, private objService: ObjectService, private route: ActivatedRoute,
              private spinner: NgxSpinnerService) {
    this.route.params.subscribe((id) => {
      this.currentRoutID = id.publicID;
      this.routeObjects();
    });
  }

  public get tableData() {
    return this.items;
  }

  public set tableData(value) {
    this.items = value;
  }

  public routeObjects() {
    let url = 'object/';
    this.pageTitle = 'Object list';
    this.hasSummaries = false;

    if ( typeof this.currentRoutID !== 'undefined') {
      url = url + 'type/' + this.currentRoutID;
      this.hasSummaries = true;
      this.pageTitle = 'Object list typeID: ' + this.currentRoutID;
    }

    this.spinner.show();
    this.apiCallService.callGetRoute(url)
      .subscribe(
        dataArray => {
          this.tableData = dataArray.length > 0 ? dataArray : [];
          this.spinner.hide();
      });
  }
}
