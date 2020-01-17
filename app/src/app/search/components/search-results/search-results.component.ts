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
import { FormControl, FormGroup, Validators} from '@angular/forms';
import { TypeService } from '../../../framework/services/type.service';
import { ObjectService } from '../../../framework/services/object.service';
import { SearchService } from '../../../services/search.service';


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
  private searchTerm: string = '';
  private typeID: any = 'undefined';
  public records: number;

  constructor(private apiCall: ApiCallService, private typeService: TypeService, private objService: ObjectService,
              private router: Router, private spinner: NgxSpinnerService, private route: ActivatedRoute,
              private searchService: SearchService) {
    this.route.queryParams.subscribe(qParams => {
      this.searchTerm = qParams.value;
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
    // tslint:disable-next-line:only-arrow-functions
    this.router.routeReuseStrategy.shouldReuseRoute = function() {
      return false;
    };
  }

  ngOnInit(): void {
    if (this.searchTerm !== '') {
      this.searchService.countSearchResult(this.searchTerm, this.typeID).subscribe(c => {
        this.records = c;
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
        const startx = dataTablesParameters[START];
        const lenthx = dataTablesParameters[LENGTH];
        if (dataTablesParameters[SEARCH].value !== null
          && dataTablesParameters[SEARCH].value !== ''
          && dataTablesParameters[SEARCH].value !== undefined) {
          that.searchService.getSearchresults(dataTablesParameters[SEARCH].value, startx, lenthx, 0, this.typeID)
            .subscribe(resp => {
              that.results = resp;
              that.records = that.results.length;
              callback({
                data: [],
                recordsTotal: this.records,
                recordsFiltered: this.records,
              });
          });
        } else {
          that.searchService.getSearchresults(this.searchTerm, startx, lenthx, 0, this.typeID).subscribe(resp => {
            that.results = resp;
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
      },
      columnDefs: [
        { width: '5%', targets: [0, 1, 2] },
        { width: '8%', targets: [-1, -2, 3 ]},
      ],
    };
  }

  public getResponse() {
    this.reload();
  }

  public reload() {
    this.searchTerm =  this.searchForm.get('term').value;
    this.typeID = this.searchForm.get('type').value == null ? 'undefined' : this.searchForm.get('type').value.public_id;

    this.searchService.countSearchResult(this.searchTerm, this.typeID).subscribe(lenx => {
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
