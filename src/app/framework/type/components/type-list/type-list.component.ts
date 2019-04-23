import { Component, OnInit } from '@angular/core';
import { CmdbType } from '../../../models/cmdb-type';
import { TypeService } from '../../../services/type.service';
import { Subject } from 'rxjs';

@Component({
  selector: 'cmdb-type-list',
  templateUrl: './type-list.component.html',
  styleUrls: ['./type-list.component.scss']
})
export class TypeListComponent implements OnInit {

  private typeList: CmdbType[] = [];
  public dtOptions: DataTables.Settings = {};
  dtTrigger: Subject<any> = new Subject();

  constructor(private typeService: TypeService) { }

  ngOnInit() {
    this.dtOptions = {
      ordering: true,
      order: [[5, 'asc']]
    };

    this.typeService.listObservable.subscribe((list: CmdbType[]) => {
      this.typeList = this.typeList.concat(list);
      this.dtTrigger.next();
    });

  }


}
