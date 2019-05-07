import { Component, OnInit } from '@angular/core';
import {FormControl} from "@angular/forms";
import {ApiCallService} from "../../../services/api-call.service";
import {TypeService} from "../../../framework/services/type.service";
import {Router} from "@angular/router";
import {SearchService} from "../../../search/search.service";

@Component({
  selector: 'cmdb-search-bar',
  templateUrl: './search-bar.component.html',
  styleUrls: ['./search-bar.component.scss']
})
export class SearchBarComponent implements OnInit {



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
