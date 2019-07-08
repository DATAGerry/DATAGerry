import { Component, OnInit } from '@angular/core';
import { CmdbType } from '../../../models/cmdb-type';
import { ApiCallService } from '../../../../services/api-call.service';
import { ActivatedRoute } from '@angular/router';
import { Modes } from '../../builder/modes.enum';

@Component({
  selector: 'cmdb-type-edit',
  templateUrl: './type-edit.component.html',
  styleUrls: ['./type-edit.component.scss']
})
export class TypeEditComponent implements OnInit {

  public typeID: number;
  public typeInstance: CmdbType;
  public mode: number = Modes.Edit;

  constructor(private api: ApiCallService, private route: ActivatedRoute) {
    this.route.params.subscribe((id) => this.typeID = id.publicID);
  }

  public ngOnInit(): void {
    this.api.callGetRoute<CmdbType>('type/' + `${this.typeID}`)
      .subscribe((typeInstance: CmdbType) => this.typeInstance = typeInstance);
  }

}
