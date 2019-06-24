import { Component, Input, OnInit } from '@angular/core';
import { ObjectService } from '../../../../../services/object.service';
import { CmdbObject } from '../../../../../models/cmdb-object';

@Component({
  selector: 'cmdb-type-tab-object-list',
  templateUrl: './type-tab-object-list.component.html',
  styleUrls: ['./type-tab-object-list.component.scss']
})
export class TypeTabObjectListComponent implements OnInit {

  @Input() typeID: number;
  public objectList: CmdbObject[];

  constructor(private objectService: ObjectService) {
    this.objectList = this.objectService.objectList;
  }

  ngOnInit() {

  }

}
