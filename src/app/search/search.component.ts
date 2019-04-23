import { Component, OnInit } from '@angular/core';
import { ApiCallService } from '../services/api-call.service';

@Component({
  selector: 'cmdb-search',
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.scss']
})
export class SearchComponent implements OnInit {

  responseresult = {}

  constructor(private _apiCallService: ApiCallService) { }

  ngOnInit() {

  }

  public getResponsResult(){
    this.responseresult = this._apiCallService.callGetRoute("/search/green").subscribe(
      params => {
        this.responseresult = params
      }
    );
  }



}
