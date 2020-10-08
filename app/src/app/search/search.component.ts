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
import { BehaviorSubject, ReplaySubject, Subject } from 'rxjs';
import { SearchResultList } from './models/search-result';
import { HttpParams } from '@angular/common/http';
import { NgxSpinnerService } from 'ngx-spinner';
import { JwPaginationComponent } from 'jw-angular-pagination';
import { takeUntil } from 'rxjs/operators';

@Component({
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.scss']
})
export class SearchComponent implements OnInit, OnDestroy {

  /**
   * Get the form control of the input field.
   */
  public get input(): AbstractControl {
    return this.searchInputForm.get('input');
  }

  /**
   * Default page size
   */
  private readonly defaultLimit: number = 10;

  /**
   * Results skipped for pagination.
   * Will be something like: skip = limit * (page-1).
   */
  private skip: number = 0;

  /**
   * Used page size.
   * Max number of displayed results.
   */
  public limit: number = this.defaultLimit;

  /**
   * Current page number.
   */
  public currentPage: number = 1;

  /**
   * Max number of size for pagination truncate.
   */
  public maxNumberOfSites: number[];


  @ViewChild('paginationComponent', { static: false }) pagination: JwPaginationComponent;
  private initSearch: boolean = true;
  private initFilter: boolean = true;

  /**
   * Search form input group.
   */
  public searchInputForm: FormGroup;

  /**
   * List of search results.
   */
  public searchResultList: SearchResultList;
  public filterResultList: any[];

  /**
   * Query parameters.
   */
  public queryParameters: any = [];

  /**
   * Resolve flag.
   */
  public resolve: BehaviorSubject<boolean> = new BehaviorSubject<boolean>(false);

  /**
   * Component un-subscriber.
   */
  private subscriber: ReplaySubject<void> = new ReplaySubject<void>();

  /**
   * Constructor of SearchComponent
   *
   * @param route Current activated route.
   * @param spinner Spinner service.
   * @param searchService API Search service.
   */
  constructor(private route: ActivatedRoute, private spinner: NgxSpinnerService, private searchService: SearchService) {
    this.searchInputForm = new FormGroup({
      input: new FormControl('', Validators.required)
    });
  }

  public ngOnInit(): void {

    this.route.queryParamMap.pipe(takeUntil(this.subscriber)).subscribe(params => {
      this.queryParameters = params.get('query');
      if (params.has('resolve')) {
        this.resolve = JSON.parse(params.get('resolve'));
      }
      this.initSearch = true;
      this.initFilter = true;
      this.onSearch();
    });

    this.resolve.asObservable().pipe(takeUntil(this.subscriber)).subscribe((change: boolean) => {
      this.onSearch();
    });
  }

  /**
   * Triggers the actual search api call.
   */
  public onSearch(): void {
    this.spinner.show();
    let params = new HttpParams();
    params = params.set('limit', this.limit.toString());
    params = params.set('skip', this.skip.toString());
    if (this.resolve.value) {
      params = params.set('resolve', this.resolve.value.toString());
    }
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

  /**
   * Pagination page was changed.
   * @param event: Data from the change event.
   */
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
    this.initFilter = value.rebuild;
    this.onSearch();
  }

  public ngOnDestroy(): void {
    this.subscriber.next();
    this.subscriber.complete();
  }
}
