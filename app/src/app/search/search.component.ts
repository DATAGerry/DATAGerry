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

import { Component, OnDestroy, OnInit } from '@angular/core';
import { SearchService } from './search.service';
import { AbstractControl, FormControl, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute } from '@angular/router';
import { Subscription } from 'rxjs';
import { SearchResultList } from './models/search-result';
import { HttpParams } from '@angular/common/http';
import { NgxSpinnerService } from 'ngx-spinner';

@Component({
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.scss']
})
export class SearchComponent implements OnInit, OnDestroy {

  // Form
  public searchInputForm: FormGroup;
  // Results
  public searchResultList: SearchResultList;
  // Parameters
  public queryParameters: any = [];
  // Subscription
  private queryParameterSubscription: Subscription;

  constructor(private route: ActivatedRoute, private spinner: NgxSpinnerService, private searchService: SearchService) {
    this.queryParameterSubscription = new Subscription();
    this.searchInputForm = new FormGroup({
      input: new FormControl('', Validators.required)
    });
  }

  public ngOnInit(): void {
    this.queryParameterSubscription = this.route.queryParamMap.subscribe(params => {
      this.queryParameters = params.get('query');
      this.onSearch();
    });
  }

  public get input(): AbstractControl {
    return this.searchInputForm.get('input');
  }

  public onSearch(): void {
    this.spinner.show();
    let params = new HttpParams();
    params = params.set('limit', '0');
    params = params.set('skip', '0');
    this.searchService.postSearch(this.queryParameters, params).subscribe((results: SearchResultList) => {
      this.searchResultList = results;
      this.spinner.hide();
    });
  }

  public ngOnDestroy(): void {
    this.queryParameterSubscription.unsubscribe();
  }

}
