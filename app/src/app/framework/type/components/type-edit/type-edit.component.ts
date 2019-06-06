import { Component, OnInit } from '@angular/core';
import { CmdbType } from '../../../models/cmdb-type';
import { ApiCallService } from '../../../../services/api-call.service';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'cmdb-type-edit',
  templateUrl: './type-edit.component.html',
  styleUrls: ['./type-edit.component.scss']
})
export class TypeEditComponent implements OnInit {

  private typeID: number;
  private typeInstance: CmdbType;

  constructor(private api: ApiCallService, private route: ActivatedRoute) {
    this.route.params.subscribe((id) => this.typeID = id.publicID);
  }

  public ngOnInit(): void {
    this.api.callGetRoute<CmdbType>('type/' + `${this.typeID}`)
      .subscribe((typeInstance: CmdbType) => this.typeInstance = typeInstance);
  }

}
