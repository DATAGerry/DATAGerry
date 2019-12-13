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

import {AfterViewInit, Component, OnDestroy, OnInit, ViewChild} from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { NgxSpinnerService } from 'ngx-spinner';
import { ApiCallService } from '../../../services/api-call.service';
import { RenderResult } from '../../../framework/models/cmdb-render';
import { Subject } from 'rxjs';
import { DataTableDirective } from 'angular-datatables';
import {FormControl, FormGroup, Validators} from '@angular/forms';
import {TypeService} from '../../../framework/services/type.service';
import {ObjectService} from "../../../framework/services/object.service";


@Component({
  selector: 'cmdb-results-search',
  templateUrl: './search-results.component.html',
  styleUrls: ['./search-results.component.scss']
})

export class SearchResultsComponent implements AfterViewInit, OnDestroy, OnInit {

  @ViewChild(DataTableDirective, {static: false})
  public dtElement: DataTableDirective;
  public dtOptions: any = {};
  public dtTrigger: Subject<any> = new Subject();

  public results: RenderResult[] = [];
  public searchForm: FormGroup;
  public typeList: any[];
  private url: any;
  private param: any = {value: ''};
  public records: number;

  constructor(private apiCall: ApiCallService, private typeService: TypeService, private objService: ObjectService,
              private router: Router, private spinner: NgxSpinnerService, private route: ActivatedRoute) {
    this.route.queryParams.subscribe(qParams => {
      this.url = 'search/';
      this.param.value = qParams.value;

      this.typeService.getTypeList().subscribe((list) => {
        this.typeList = list;
      });
      if (qParams.value === '') {
        this.objService.countObjects().subscribe(count => this.records = count);
      }

      this.searchForm = new FormGroup({
        term: new FormControl('', Validators.required),
        type: new FormControl( null, Validators.required),
        active: new FormControl( false, Validators.required),
      });
    });
    this.router.routeReuseStrategy.shouldReuseRoute = function () {
      return false;
    };
  }

  ngOnInit(): void {
    if (this.param.value !== '') {

      this.apiCall.callGetRoute('search/count/', {params: this.param}).subscribe(test => {
        this.records = test;
      });
    }
    this.callObjects();
  }

  public callObjects() {
    const that = this;
    const START = 'start';
    const LENGTH = 'length';
    const SEARCH = 'search';
    this.dtOptions = {
      dom: '<"row" <"col-sm-3" l><"col" f> >' +
        '<"row" <"col-sm-12"tr>>' +
        '<\"row\" <\"col-sm-12 col-md-5\"i> <\"col-sm-12 col-md-7\"p> >',
      pagingType: 'full_numbers',
      serverSide: true,
      processing: true,
      ordering: false,
      ajax: (dataTablesParameters: RenderResult[], callback) => {
        that.param[START] = dataTablesParameters[START];
        that.param[LENGTH] = dataTablesParameters[LENGTH];

        if (dataTablesParameters[SEARCH].value !== null
          && dataTablesParameters[SEARCH].value !== ''
          && dataTablesParameters[SEARCH].value !== undefined) {
          const was = 'object/filter/' + dataTablesParameters[SEARCH].value;
          that.apiCall.callGetRoute(this.url, {params: that.param}).subscribe(resp => {
            that.results = resp === null ? [] : resp;
            callback({
              data: [],
              recordsTotal: that.results.length,
              recordsFiltered: that.results.length,
            });
          });
        } else {
          that.apiCall.callGetRoute(this.url, {params: that.param}).subscribe(resp => {
            that.results = resp === null ? [] : resp;
            callback({
              data: [],
              recordsTotal: that.records,
              recordsFiltered: that.records,
            });
          });
        }
      },
      order: [[1, 'asc']],
      language: {
        search: '',
        searchPlaceholder: 'Filter...'
      }
    };
  }

  public getResponse() {
    this.reload();
  }

  public reload() {
    const searchTerm = this.searchForm.get('term').value;
    const typeID = this.searchForm.get('type').value == null ? 'undefined' : this.searchForm.get('type').value.public_id;
    const objectState = this.searchForm.get('active').value;

    this.param.value = searchTerm;
    this.param.type_id = typeID;
    this.param.active = objectState;

    const newParams = {params: {value: searchTerm, type_id: typeID}}
    this.apiCall.callGetRoute('search/count/', newParams).subscribe(lenx => {
      this.records = lenx;
    });

    this.dtElement.dtInstance.then((dtInstance: DataTables.Api) => {
      dtInstance.destroy();
      this.dtTrigger.next();
    });
  }

  public rerender(): void {
    if (typeof this.dtElement !== 'undefined' && typeof this.dtElement.dtInstance !== 'undefined') {
      this.dtElement.dtInstance.then((dtInstance: DataTables.Api) => {
        // Destroy the table first
        dtInstance.destroy();
      });
    }
  }

  ngAfterViewInit(): void {
    this.dtTrigger.next();
  }

  ngOnDestroy(): void {
    // Do not forget to unsubscribe the event
    this.dtTrigger.unsubscribe();

    // If a table is initialized while it is hidden,
    // the browser calculates the width of the columns
    this.dtElement.dtInstance.then((dtInstance: any) => {
      dtInstance.columns.adjust()
        .responsive.recalc();
    });
  }
}
