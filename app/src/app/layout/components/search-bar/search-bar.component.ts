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

import { Component, OnInit } from '@angular/core';
import { FormControl } from '@angular/forms';
import { TypeService } from '../../../framework/services/type.service';
import { Router } from '@angular/router';
import { debounceTime, map } from 'rxjs/operators';
import { ApiCallService } from '../../../services/api-call.service';

@Component({
  selector: 'cmdb-search-bar',
  templateUrl: './search-bar.component.html',
  styleUrls: ['./search-bar.component.scss'],
})

export class SearchBarComponent implements OnInit {

  public searchCtrl: FormControl = new FormControl('');
  public autoResult: any[] = [];
  public categoryList = [{label: 'Categories'}];
  public category = 'Categories';
  private typeID: string = 'undefined';
  private url: string = '/search/?value=';

  constructor(
    private typeService: TypeService,
    private route: Router,
    private api: ApiCallService) {
  }

  ngOnInit() {
    this.typeService.getTypeList().subscribe((list) => {
      this.categoryList = this.categoryList.concat(list);
    }, error => {
      this.route.navigate(['login/']);
    });
    this.autoSearch();
  }

  public autoSearch() {
    this.searchCtrl.valueChanges.subscribe( () => {
      if (typeof this.searchCtrl.value === 'string' && this.searchCtrl.value.length > 0) {
        this.api.callGetRoute(this.url + this.searchCtrl.value + '&type_id=' + this.typeID, {params: {limit: '5'}})
          .pipe(
            debounceTime(500),  // WAIT FOR 500 MILISECONDS AFTER EACH KEY STROKE.
            map(
              (data: any) => {
                return (
                  data.length > 0 ? data as any[] : [{object: 'No Object Found'} as any]
                );
              }
            )).subscribe( value => {
                this.autoResult = value as [];
        });
      }
    });
  }

  public getResponse() {
    this.hiden();
    this.route.navigate(['search/results'], {queryParams: {value: this.searchCtrl.value} });
  }

  public highlight(value) {
    if (typeof value === 'string' && value.length > 0) {
      return value.replace(new RegExp(this.searchCtrl.value, 'gi'), match => {
        return '<span class="badge badge-secondary">' + match + '</span>';
      });
    }
  }

  public hiden() {
    setTimeout(() => {
      this.searchCtrl.setValue('');
    }, 300);
  }

  public dropdownMenu(element) {
    this.category = element.label;
    this.typeID = this.getAppropriateTypeId(this.categoryList, this.category);
  }

  private getAppropriateTypeId(object, value) {
    const item = object.find(i => i.label === value);
    return item.public_id;
  }

}
