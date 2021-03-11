/*
* DATAGERRY - OpenSource Enterprise CMDB
* Copyright (C) 2019 - 2021 NETHINKS GmbH
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
* along with this program. If not, see <https://www.gnu.org/licenses/>.
*/

import { Component, OnDestroy, OnInit, ViewChild } from '@angular/core';
import { SearchService } from './search.service';
import { AbstractControl, FormControl, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { BehaviorSubject, ReplaySubject } from 'rxjs';
import { SearchResultList } from './models/search-result';
import { HttpParams } from '@angular/common/http';
import { JwPaginationComponent } from 'jw-angular-pagination';
import { takeUntil } from 'rxjs/operators';
import { ProgressSpinnerService } from '../layout/progress/progress-spinner.service';
import { PageLengthEntry } from '../layout/table/components/table-page-size/table-page-size.component';

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
  private skipRef: number = 0;

  /**
   * Used page size.
   * Max number of displayed results.
   */
  public limit: number = this.defaultLimit;

  /**
   * Current page number.
   */
  public currentPage: number = 1;
  public currentPageRef: number = 1;

  /**
   * Max number of size for pagination truncate.
   */
  public maxNumberOfSites: number[];
  public maxNumberOfSitesRef: number[];


  @ViewChild('paginationComponentRef') paginationRef: JwPaginationComponent;
  private initSearchRef: boolean = true;
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
  public publicIdResult;
  public filterResultList: any[];

  /**
   * List of reference results
   */
  public referenceResultList: SearchResultList;

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
   * A preset of default page sizes.
   * @private
   */
  public readonly defaultResultSizeList: Array<PageLengthEntry> =
    [
      { label: '10', value: 10 },
      { label: '25', value: 25 },
      { label: '50', value: 50 },
      { label: '100', value: 100 },
      { label: '200', value: 200 }
    ];

  /**
   * Page size select form group.
   */
  public resultSizeForm: FormGroup = new FormGroup({
    size: new FormControl(this.limit),
  });

  /**
   * Constructor of SearchComponent
   */
  constructor(private route: ActivatedRoute, private searchService: SearchService,
              private spinner: ProgressSpinnerService, private router: Router) {
    this.searchInputForm = new FormGroup({
      input: new FormControl('', Validators.required)
    });
  }

  public ngOnInit(): void {

    this.route.queryParamMap.pipe(takeUntil(this.subscriber)).subscribe(params => {
      this.queryParameters = params.get('query');
      if (params.has('resolve')) {
        this.resolve.next(JSON.parse(params.get('resolve')));
      }
      if (params.has('limit')) {
        this.limit = (+JSON.parse(params.get('limit')));
        this.resultSizeForm.get('size').setValue(this.limit);
      }
      this.initSearchRef = true;
      this.initSearch = true;
      this.initFilter = true;
      this.onSearch();
    });

    this.resolve.asObservable().pipe(takeUntil(this.subscriber)).subscribe((change) => {
      this.referencesSearch(change);
    });

    this.resultLength.valueChanges.pipe(takeUntil(this.subscriber))
      .subscribe((size: number) => {
        this.limit = size;
        this.router.navigate(
          [],
          {
            relativeTo: this.route,
            queryParams: { limit: this.limit },
            queryParamsHandling: 'merge'
          });
        this.onSearch();
      });
  }

  /**
   * Get the form control of the size selection.
   */
  public get resultLength(): FormControl {
    return this.resultSizeForm.get('size') as FormControl;
  }

  /**
   * Trigger the resolve search api call
   */

  public referencesSearch(change: boolean = false) {
    if (change && this.searchResultList) {
      this.spinner.show('app', 'Searching...');
      let params = new HttpParams();
      params = params.set('limit', this.limit.toString());
      params = params.set('skip', this.skipRef.toString());

      const typIDs: number[] = [];
      const objIDs: number [] = [];
      for (const obj of this.searchResultList.results) {
        typIDs.push(obj.result.type_information.type_id);
        objIDs.push(obj.result.object_information.object_id);
      }

      if (this.publicIdResult) {
        typIDs.push(this.publicIdResult.result.type_information.type_id);
        objIDs.push(this.publicIdResult.result.object_information.object_id);
      }

      const query = [
        {
          $lookup: {
            from: 'framework.types',
            localField: 'type_id',
            foreignField: 'public_id',
            as: 'type'
          }
        },
        {
          $unwind: {
            path: '$type'
          }
        },
        {
          $match: {
            $and: [
              { 'type.fields.type': 'ref' },
              {
                $or: [
                  { 'type.fields.ref_types': { $in: typIDs } }]
              }
            ]
          }
        },
        {
          $match: {
            'fields.value': { $in: objIDs }
          }
        }
      ];
      params = params.set('resolve', this.resolve.value.toString());
      params = params.set('query', JSON.stringify(query));

      this.searchService.getSearch(this.queryParameters, params).pipe(takeUntil(this.subscriber))
        .subscribe((results: SearchResultList) => {
            this.referenceResultList = results;
            if (this.initSearchRef && this.referenceResultList) {
              this.maxNumberOfSitesRef = Array.from({ length: (this.referenceResultList.total_results) }, (v, k) => k + 1);
              this.initSearchRef = false;
            }
            if (!this.referenceResultList || this.referenceResultList.total_results === 0) {
              this.resolve.next(false);
            }
          }, (error) => console.log(error),
          () => this.spinner.hide('app'));
    }
  }

  /**
   * Triggers the actual search api call.
   */
  public onSearch(): void {
    this.publicIdResult = undefined;
    this.spinner.show('app', 'Searching...');
    let params = new HttpParams();
    params = params.set('limit', this.limit.toString());
    params = params.set('skip', this.skip.toString());
    this.searchService.postSearch(this.queryParameters, params).pipe(takeUntil(this.subscriber)).subscribe((results: SearchResultList) => {
        this.searchResultList = results;
        this.filterResultList = this.initFilter && results !== null ? results.groups : this.filterResultList;
        if (this.initSearch) {
          this.maxNumberOfSites = Array.from({ length: (this.searchResultList.total_results) }, (v, k) => k + 1);
          this.initSearch = false;
          this.initFilter = false;
        }
      }, (error => console.log(error)),
      () => {
        this.initSearchRef = true;
        this.resolve.next(true);
      });
    let localParameters = JSON.parse(this.queryParameters);
    if (localParameters.length === 1) {
      localParameters[0].searchForm = 'publicID';
      localParameters = JSON.stringify(localParameters);
      this.searchService.postSearch(localParameters, params).pipe(takeUntil(this.subscriber)).subscribe((results: SearchResultList) => {
        if (results !== null && results.results.length > 0) {
          this.publicIdResult = results.results[0];
        }
      }).add(() => this.spinner.hide('app'));
    } else {
      this.spinner.hide('app');
    }
  }

  /**
   * Pagination page was changed.
   * @param event: Data from the change event.
   */
  public onChangePageRef(event): void {
    this.currentPageRef = event;
    this.skipRef = ((this.currentPageRef === 0 ? 1 : this.currentPageRef) - 1) * this.limit;
    this.referencesSearch(true);
  }

  /**
   * Pagination page was changed.
   * @param event: Data from the change event.
   */
  public onChangePage(event): void {
    this.currentPage = event;
    this.skip = (this.currentPage - 1) * this.limit;
    this.onSearch();

  }

  public reSearch(value: any) {
    this.queryParameters = JSON.stringify(value.query);
    this.initSearchRef = true;
    this.initSearch = true;
    this.initFilter = value.rebuild;
    this.onSearch();
  }

  public ngOnDestroy(): void {
    this.subscriber.next();
    this.subscriber.complete();
  }
}
