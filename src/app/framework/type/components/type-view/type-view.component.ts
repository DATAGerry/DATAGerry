import { Component, OnInit } from '@angular/core';
import { ApiCallService } from '../../../../services/api-call.service';
import { ActivatedRoute } from '@angular/router';
import { CmdbType } from '../../../models/cmdb-type';

@Component({
  selector: 'cmdb-type-view',
  templateUrl: './type-view.component.html',
  styleUrls: ['./type-view.component.scss']
})
export class TypeViewComponent implements OnInit {

  private typeID: number;
  private typeInstance: CmdbType;

  constructor(private api: ApiCallService, private route: ActivatedRoute) {
    this.route.params.subscribe((id) => this.typeID = id.publicID);
  }

  ngOnInit() {
    this.api.callGetRoute<CmdbType>('type/' + `${this.typeID}`)
      .subscribe((typeInstance: CmdbType) => this.typeInstance = typeInstance);
  }

}
