import { Component, OnDestroy, OnInit, ViewChild } from '@angular/core';
import { GroupService } from '../../services/group.service';
import { Group } from '../../models/group';
import { DataTableDirective } from 'angular-datatables';
import { Subject } from 'rxjs';
import { Right } from '../../models/right';
import { RightService } from '../../services/right.service';

@Component({
  selector: 'cmdb-groups-list',
  templateUrl: './groups-list.component.html',
  styleUrls: ['./groups-list.component.scss']
})
export class GroupsListComponent implements OnInit, OnDestroy {

  public groupList: Group[];
  public rightList: Right[];

  public dtOptions: DataTables.Settings = {};
  public dtTrigger: Subject<any> = new Subject();

  constructor(private groupService: GroupService, private rightService: RightService) {
  }

  public ngOnInit(): void {
    this.dtOptions = {
      language: {
        search: '',
        searchPlaceholder: 'Filter...'
      }
    };

    this.groupService.getGroupList().subscribe((groupList: Group[]) => {
        this.groupList = groupList;
      },
      (error) => {
        console.error(error);
      }, () => {
        this.dtTrigger.next();
      }
    );

    this.rightService.getRightList().subscribe((rightList: Right[]) => {
      this.rightList = rightList;
    });
  }

  public ngOnDestroy(): void {
    this.dtTrigger.unsubscribe();
  }

}
