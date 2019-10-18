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

import {Component, OnDestroy, ViewChild} from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { NgxSpinnerService } from 'ngx-spinner';
import { ApiCallService } from '../../../services/api-call.service';
import { RenderResult } from '../../../framework/models/cmdb-render';
import { Subject } from 'rxjs';
import { DataTableDirective } from 'angular-datatables';
import {FormControl, FormGroup, Validators} from '@angular/forms';
import {TypeService} from '../../../framework/services/type.service';


@Component({
  selector: 'cmdb-results-search',
  templateUrl: './search-results.component.html',
  styleUrls: ['./search-results.component.scss']
})

export class SearchResultsComponent implements OnDestroy {

  @ViewChild(DataTableDirective, {static: false})
  public dtElement: DataTableDirective;
  public dtOptions: any = {};
  public dtTrigger: Subject<any> = new Subject();

  public results: RenderResult[] = [];
  public searchForm: FormGroup;
  public typeList: any[];
  private url: any;

  constructor(private apiCall: ApiCallService, private typeService: TypeService,
              private router: Router, private spinner: NgxSpinnerService, private route: ActivatedRoute) {
    this.route.queryParams.subscribe(qParams => {
      this.url = 'search/?value=' + qParams.value;

      this.typeService.getTypeList().subscribe((list) => {
        this.typeList = list;
      }, error => {},
        () => { this.callObjects(); });

      this.searchForm = new FormGroup({
        term: new FormControl('', Validators.required),
        type: new FormControl( null, Validators.required),
        active: new FormControl( false, Validators.required),
      });
    });
  }

  private callObjects() {
    this.spinner.show();
    this.loadDatatable();

    this.apiCall.callGetRoute(this.url).subscribe(
      (data: RenderResult[]) => {
        this.results = data;
        this.rerender();
      },
      (err) => {
        console.error(err);
      },
      () => {
        this.dtTrigger.next();
        this.spinner.hide();
      });
  }

  private loadDatatable() {
    this.dtOptions = {
      ordering: true,
      order: [[1, 'asc']],
      dom:
        '<"row" <"col-sm-2" l> <"col-sm-3" B > <"col" f> >' +
        '<"row" <"col-sm-12"tr>>' +
        '<\"row\" <\"col-sm-12 col-md-5\"i> <\"col-sm-12 col-md-7\"p> >',
      buttons: [
        {
          text: '<i class="fas fa-plus"></i> Add',
          className: 'btn btn-success btn-sm mr-1',
          action: function() {
            this.router.navigate(['/framework/type/add']);
          }.bind(this)
        }
      ],
      language: {
        search: '',
        searchPlaceholder: 'Filter...'
      }
    };
  }

  public getResponse() {
    const searchTerm = this.searchForm.get('term').value;
    const typeID = this.searchForm.get('type').value == null ? 'undefined' : this.searchForm.get('type').value.public_id;
    const objectState = this.searchForm.get('active').value;
    this.url = 'search/?value=' + searchTerm + '&type_id=' + typeID + '&active=' + objectState;
    this.callObjects();
  }

  public rerender(): void {
    if (typeof this.dtElement !== 'undefined' && typeof this.dtElement.dtInstance !== 'undefined') {
      this.dtElement.dtInstance.then((dtInstance: DataTables.Api) => {
        // Destroy the table first
        dtInstance.destroy();
      });
    }
  }

  public ngOnDestroy(): void {
    this.dtTrigger.unsubscribe();
  }
}
