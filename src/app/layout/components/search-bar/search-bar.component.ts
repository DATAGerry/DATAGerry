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
import { ShareDataService } from '../../../services/share-data.service';

@Component({
  selector: 'cmdb-search-bar',
  templateUrl: './search-bar.component.html',
  styleUrls: ['./search-bar.component.scss'],
})

export class SearchBarComponent implements OnInit {

  searchCtrl: FormControl = new FormControl('');
  autoResult = [];
  categoryList = [{label: 'Categories'}];
  category = 'Categories';
  typeID: string = 'undefined';

  constructor(
    private typeService: TypeService,
    private route: Router,
    private sApi: ShareDataService) {
  }

  ngOnInit() {
    this.typeService.getTypeList().subscribe((list) => {
      this.categoryList = this.categoryList.concat(list);
    }, error => {
      /*
      * Here it must be considered how this should be treated
      * */
      this.route.navigate(['login/']);
    });
    this.autosearch();
  }

  public hiden() {
    setTimeout(() => {
      this.searchCtrl.setValue('');
    }, 300);
  }

  public autosearch() {
    this.searchCtrl.valueChanges.subscribe( data => {
      this.apiCall(5);
    }, error => {
    }, () => {
    });
  }

  public getResponse() {
    this.sApi.searchTerm('/search/?value=' + this.searchCtrl.value + '&type_id=' + this.typeID + '&limit=' + 0).subscribe(
      data => {
        this.sApi.setDataResult(data);
      });
    this.route.navigate(['search/results']);
  }

  private apiCall(limit) {
    if (typeof this.searchCtrl.value === 'string' && this.searchCtrl.value.length > 0) {
      this.sApi.searchTerm('/search/?value=' + this.searchCtrl.value + '&type_id=' + this.typeID + '&limit=' + limit).subscribe(
        data => {
          this.autoResult = data as [];
        });
    }
  }

  public highlight(value) {
    if (typeof value === 'string' && value.length > 0) {
      return value.replace(new RegExp(this.searchCtrl.value, 'gi'), match => {
        return '<span class="badge badge-secondary">' + match + '</span>';
      });
    }
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
