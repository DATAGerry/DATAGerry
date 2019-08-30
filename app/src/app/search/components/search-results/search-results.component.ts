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

import { Component } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { NgxSpinnerService } from 'ngx-spinner';
import { ApiCallService } from '../../../services/api-call.service';
import {RenderResult} from '../../../framework/models/cmdb-render';
import { TableColumnAction } from '../../../layout/components/table/models/table-columns-action';


@Component({
  selector: 'cmdb-results-search',
  templateUrl: './search-results.component.html',
  styleUrls: ['./search-results.component.scss']
})

export class SearchResultsComponent {

  public results: RenderResult[] = [];
  public thColumnsActions: TableColumnAction[];
  private url: any;

  constructor(private apiCallService: ApiCallService, private router: Router, private spinner: NgxSpinnerService,
              private route: ActivatedRoute) {

    this.route.queryParams.subscribe(qParams => {
      this.url = 'search/?value=' + qParams.value;
      this.callObjects();
    });
  }

  private callObjects() {
    this.apiCallService.callGetRoute(this.url).subscribe(
      (data: RenderResult[]) => {
        this.spinner.show();
        setTimeout( () => {
          this.results = data;
          this.spinner.hide();
        }, 100);
      });
    this.thColumnsActions = [
      { name: 'view', classValue: 'text-dark ml-1', linkRoute: '/framework/object/view/', fontIcon: 'fa fa-eye', active: true}];
  }

}
