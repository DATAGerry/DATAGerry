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

import {Component, OnInit, ViewChild} from '@angular/core';
import { ApiCallService } from '../services/api-call.service';
import { FormControl } from '@angular/forms';
import { Subject } from "rxjs";
import { DataTableDirective } from "angular-datatables";
import { TypeService } from "../framework/services/type.service";

@Component({
  selector: 'cmdb-search',
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.scss']
})
export class SearchComponent implements OnInit {

  @ViewChild(DataTableDirective)
  public dtElement: DataTableDirective;

  public dtOptions: DataTables.Settings = {};
  public dtTrigger: Subject<any> = new Subject();

  searchCtrl: FormControl = new FormControl('');
  autoResult = <any>[];
  endResult = <any>[];
  categoryList = <any>[{label : "Categories"}];

  category = "Categories";
  typ_id: string = "undefined"

  constructor(private _apiCallService: ApiCallService, private _typService: TypeService) { }


  ngOnInit() {

    this.dtOptions = {
      ordering: true,
      order: [[1, 'asc']],
      language: {
        search: "",
        searchPlaceholder: "Filter..."
      }
    };
    this.dtTrigger.next();

    this._typService.getTypeList().subscribe((list) => {
      this.categoryList = this.categoryList.concat(list);
      });
  }


  public autosearch(){
    this.searchCtrl.valueChanges.subscribe(
      term => {
        if (term != '') {
          this.apiCall(term,5);
        }else {
          this.autoResult = <any>[];
        }
      })
  }


  public getResponse(){

    this._apiCallService.searchTerm("/search/?value="+this.searchCtrl.value+"&type_id="+this.typ_id+"&limit="+0).subscribe(
      data => {
        this.endResult = data as any[];
      },
      () => {

      },
      () => {
        this.rerender();
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

  ngAfterViewInit(): void {
    this.dtTrigger.next();
  }

  ngOnDestroy(): void {
    // Do not forget to unsubscribe the event
    this.dtTrigger.unsubscribe();
  }

  rerender(): void {
    this.dtElement.dtInstance.then((dtInstance: DataTables.Api) => {
      // Destroy the table first
      dtInstance.destroy();
      // Call the dtTrigger to rerender again
      this.dtTrigger.next();
    });
  }
}
