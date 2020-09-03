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

import { Component, OnDestroy, OnInit, ViewChild } from '@angular/core';
import { SearchService } from './search.service';
import { AbstractControl, FormControl, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute } from '@angular/router';
import { Subscription } from 'rxjs';
import { SearchResultList } from './models/search-result';
import { HttpParams } from '@angular/common/http';
import { NgxSpinnerService } from 'ngx-spinner';
import { JwPaginationComponent } from 'jw-angular-pagination';

@Component({
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.scss']
})
export class SearchComponent implements OnInit, OnDestroy {

  constructor(private route: ActivatedRoute, private spinner: NgxSpinnerService, private searchService: SearchService) {
    this.queryParameterSubscription = new Subscription();
    this.searchInputForm = new FormGroup({
      input: new FormControl('', Validators.required)
    });
  }

  public get input(): AbstractControl {
    return this.searchInputForm.get('input');
  }

  // Pagination
  private readonly defaultLimit: number = 10;
  private skip: number = 0;
  public limit: number = this.defaultLimit;
  public currentPage: number = 1;
  public maxNumberOfSites: number[];
  @ViewChild('paginationComponent', { static: false }) pagination: JwPaginationComponent;
  private initSearch: boolean = true;
  private initFilter: boolean = true;

  // Form
  public searchInputForm: FormGroup;
  // Results
  public searchResultList: SearchResultList;
  public filterResultList: any[];
  // Parameters
  public queryParameters: any = [];
  // Subscription
  private queryParameterSubscription: Subscription;

  public ngOnInit(): void {
    this.queryParameterSubscription = this.route.queryParamMap.subscribe(params => {
      this.queryParameters = params.get('query');
      this.initSearch = true;
      this.initFilter = true;
      this.onSearch();
    });
  }

  public onSearch(): void {
    this.spinner.show();
    let params = new HttpParams();
    params = params.set('limit', this.limit.toString());
    params = params.set('skip', this.skip.toString());
    this.searchService.postSearch(this.queryParameters, params).subscribe((results: SearchResultList) => {
      this.searchResultList = results;
      this.filterResultList = this.initFilter ? results.groups : this.filterResultList;
      if (this.initSearch) {
        this.maxNumberOfSites = Array.from({ length: (this.searchResultList.total_results) }, (v, k) => k + 1);
        this.initSearch = false;
        this.initFilter = false;
      }
      this.spinner.hide();
    });
  }

  public onChangePage(event): void {
    if (this.currentPage !== this.pagination.pager.currentPage) {
      this.currentPage = this.pagination.pager.currentPage;
      this.skip = (this.currentPage - 1) * this.limit;
      this.onSearch();
    }

  }

  public reSearch(value: any) {
    this.queryParameters = JSON.stringify(value.query);
    this.initSearch = true;
    this.initFilter = value.rebuild ;
    this.onSearch();
  }

  public ngOnDestroy(): void {
    this.queryParameterSubscription.unsubscribe();
  }
}
