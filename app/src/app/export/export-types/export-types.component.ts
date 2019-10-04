import { Component, OnInit, Output } from '@angular/core';
import { TypeService } from '../../framework/services/type.service';
import { CmdbType } from '../../framework/models/cmdb-type';

@Component({
  selector: 'cmdb-export-types',
  templateUrl: './export-types.component.html',
  styleUrls: ['./export-types.component.scss']
})
export class ExportTypesComponent implements OnInit {

  public typeList: CmdbType[] = [];

  constructor(private typeService: TypeService) {
  }

  public ngOnInit(): void {
    this.typeService.getTypeList().subscribe((typeList: CmdbType[]) => {
      this.typeList = typeList;
    });
  }

  public selectExportTypes(value) {
    console.log(value);
  }

}
