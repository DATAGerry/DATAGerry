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

  showResultList = false;


  constructor(
    private typeService: TypeService,
    private router: Router,
    private sApi: ShareDataService) {
  }


  ngOnInit() {

    this.typeService.getTypeList().subscribe((list) => {
      this.categoryList = this.categoryList.concat(list);
    });
  }

  public onBlurMethod() {
    this.showResultList = false;
    this.autoResult = [];
  }

  public autosearch() {
    this.searchCtrl.valueChanges.subscribe(
      term => {
        if (typeof term === 'string' && term.length > 0 && term !== undefined) {
          this.apiCall(term, 5);
        } else {
          this.autoResult = [];
        }
      });

    if (this.autoResult.length === 0) {
      this.showResultList = false;
    } else {
      this.showResultList = true;
    }
  }


  public getResponse() {

    if (typeof this.searchCtrl.value === 'string' && this.searchCtrl.value.length > 0 && this.searchCtrl.value !== undefined) {
      this.router.navigate(['search/results']);
      this.sApi.searchTerm('/search/?value=' + this.searchCtrl.value + '&type_id=' + this.typeID + '&limit=' + 0).subscribe(
        data => {
          this.sApi.setDataResult(data);

        });
    }
  }


  private apiCall(term, limit) {

    this.sApi.searchTerm('/search/?value=' + term + '&type_id=' + this.typeID + '&limit=' + limit).subscribe(
      data => {
        this.autoResult = data;
      });
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
