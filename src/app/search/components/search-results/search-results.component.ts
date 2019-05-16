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
import { SearchService } from '../../search.service';
import { Router } from '@angular/router';


@Component({
  selector: 'cmdb-results-search',
  templateUrl: './search-results.component.html',
  styleUrls: ['./search-results.component.scss']
})
export class SearchResultsComponent implements OnInit, AfterViewInit, OnDestroy {

  @ViewChild(DataTableDirective)
  public dtElement: DataTableDirective;

  public dtOptions: DataTables.Settings = {};
  public dtTrigger: Subject<any> = new Subject();

  results = [];

  constructor(private searchService: SearchService, private router: Router) {

  }

  ngOnInit() {

  }

  ngAfterViewInit(): void {
    this.searchService.getSearchResult().subscribe(temp => {
        this.results = temp as [];
      },
      () => {

      },
      () => {
        this.dtOptions = {
          ordering: true,
          order: [[1, 'asc']],
          language: {
            search: '',
            searchPlaceholder: 'Filter...'
          }
        };
        this.dtTrigger.next();
      });
  }

  ngOnDestroy(): void {
    // Do not forget to unsubscribe the event
    this.dtTrigger.unsubscribe();
  }

  public rerender(): void {
    this.dtElement.dtInstance.then((dtInstance: DataTables.Api) => {
      // Destroy the table first
      dtInstance.destroy();
      // Call the dtTrigger to rerender again
      this.dtTrigger.next();
    });
  }

}
