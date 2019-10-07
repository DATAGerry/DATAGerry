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

import { Component, OnInit } from '@angular/core';
import {FormControl, FormGroup, Validators} from '@angular/forms';
import { TypeService } from '../../../framework/services/type.service';
import { Router } from '@angular/router';
import { debounceTime, map } from 'rxjs/operators';
import { ApiCallService } from '../../../services/api-call.service';
import { RenderResult } from '../../../framework/models/cmdb-render';

@Component({
  selector: 'cmdb-search-bar',
  templateUrl: './search-bar.component.html',
  styleUrls: ['./search-bar.component.scss'],
})

export class SearchBarComponent implements OnInit {

  private readonly apiURL: string = '/search/?value=';
  private searchTerm: string = '';
  private typeID: any = 'undefined';
  private objectState: boolean = false;

  public searchForm: FormGroup;
  public typeList: any[];
  public autoResult: RenderResult[] = [];

  constructor(
    private typeService: TypeService, private route: Router, private api: ApiCallService) {
    this.searchForm = new FormGroup({
      term: new FormControl(null, Validators.required),
      type: new FormControl( null, Validators.required),
      active: new FormControl( false, Validators.required),
    });
  }

  ngOnInit() {
    this.typeService.getTypeList().subscribe((list) => this.typeList = list);

    this.searchForm.valueChanges.subscribe(val => {
      this.searchTerm = val.term == null ? '' : val.term;
      this.typeID = val.type == null ? 'undefined' : val.type.public_id;
      this.objectState = val.active;
      if (this.searchTerm.length > 0) {
        this.api.callGetRoute(this.apiURL + this.searchTerm + '&type_id=' + this.typeID, {params: {limit: '5'}})
          .pipe(
            debounceTime(100)  // WAIT FOR 500 MILISECONDS AFTER EACH KEY STROKE.
          ).subscribe( (data: RenderResult[]) => this.autoResult = data);
      }
    });


    // tslint:disable-next-line:only-arrow-functions
    $(document).mouseup(function(e) {
      const popup: any = $('#search-bar-advanced');
      // @ts-ignore
      if (!$('#search-bar-advanced').is(e.target) && !popup.is(e.target) && popup.has(e.target).length === 0) {
        popup.collapse('hide');
      }
    });
  }

  public getResponse() {
    const collapseTag: any = $('.collapse');
    if (collapseTag.hasClass('show')) {
      collapseTag.collapse('hide');
    }
    this.route.navigate(['search/results'],
      {queryParams: {value: this.searchTerm, active: this.objectState, type_id: this.typeID} });
  }

  public highlight(value) {
    if (typeof value === 'string' && value.length > 0) {
      return value.replace(new RegExp(value, 'gi'), match => {
        return '<span class="badge badge-secondary">' + match + '</span>';
      });
    }
  }
}
