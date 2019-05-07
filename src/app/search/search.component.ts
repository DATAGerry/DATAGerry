/*
* Net|CMDB - OpenSource Enterprise CMDB
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

import {Component, OnInit, Input} from '@angular/core';
import { ApiCallService } from '../services/api-call.service';
import { FormControl } from '@angular/forms';
import { TypeService } from "../framework/services/type.service";
import { Router } from '@angular/router';
import {SearchService} from "./search.service";

@Component({
  selector: 'cmdb-search',
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.scss']
})
export class SearchComponent implements OnInit {

  searchCtrl: FormControl = new FormControl('');
  autoResult = <any>[];
  categoryList = <any>[{label : "Categories"}];

  category = "Categories";
  typ_id: string = "undefined";

  showResultList = false;


  constructor(private _apiCallService: ApiCallService, private _typService: TypeService, private router: Router, private _searchService:SearchService) { }


  ngOnInit() {

    this._typService.getTypeList().subscribe((list) => {
      this.categoryList = this.categoryList.concat(list);
      });
  }

  public onBlurMethod(){
    this.showResultList = false;
    this.autoResult = <any>[];
  }

  public autosearch(){
    this.searchCtrl.valueChanges.subscribe(
      term => {
        if (typeof term === "string" && term.length > 0 && term !== undefined) {
          this.apiCall(term,5);
        }else {
          this.autoResult = <any>[];
        }
      })

    if(this.autoResult.length == 0){
      this.showResultList = false;
    }else{
      this.showResultList = true;
    }

  }


  public getResponse(){

    this._apiCallService.searchTerm("/search/?value="+this.searchCtrl.value+"&type_id="+this.typ_id+"&limit="+0).subscribe(
      data => {
        this._searchService.setSearchResult(data as any[]);
        this.router.navigate(["search/results"]);
        console.log(data);
      });
  }

  public filter(arr){
    arr.forEach(function (obj) {
      Object.keys(obj).forEach(function(k){
        console.log(k + ' - ' + obj[k]);
        this.autoResult.add()
      });
    })
  }


  private apiCall(term, limit){

    this._apiCallService.searchTerm("/search/?value="+term+"&type_id="+this.typ_id+"&limit="+limit).subscribe(
      data => {
        this.autoResult = data;
      })
  }


  public dropdownMenu(element){
    this.category = element.label;
    this.typ_id = this.getAppropriateTypeId(this.categoryList, this.category);
  }


  private getAppropriateTypeId(object, value) {
    let item = object.find(item => item.label === value);
    return item.public_id;
  }

}
