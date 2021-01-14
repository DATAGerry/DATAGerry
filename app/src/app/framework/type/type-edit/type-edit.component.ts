import { Component, OnInit } from '@angular/core';
import { CmdbType } from '../../models/cmdb-type';
import { ActivatedRoute } from '@angular/router';
import { CmdbMode } from '../../modes.enum';
import { TypeService } from '../../services/type.service';

@Component({
  selector: 'cmdb-type-edit',
  templateUrl: './type-edit.component.html',
  styleUrls: ['./type-edit.component.scss']
})
export class TypeEditComponent implements OnInit {

  public typeID: number;
  public typeInstance: CmdbType;
  public mode: number = CmdbMode.Edit;

  public stepIndex: number = 0;

  constructor(private typeService: TypeService, private route: ActivatedRoute) {
    this.route.queryParams.subscribe(params => {
      this.stepIndex = params.stepIndex;
    });
    this.route.params.subscribe((id) => this.typeID = id.publicID);
  }

  public ngOnInit(): void {

    this.typeService.getType(this.typeID).subscribe((typeInstance: CmdbType) => this.typeInstance = typeInstance);

  }

}
