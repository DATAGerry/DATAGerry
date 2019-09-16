import {
  ApplicationRef,
  Component,
  ComponentFactoryResolver, Injector,
  OnDestroy,
  OnInit,
  ViewChild,
} from '@angular/core';
import { GroupService } from '../../services/group.service';
import { Group } from '../../models/group';
import { DataTableDirective } from 'angular-datatables';
import { Subject } from 'rxjs';
import { Right } from '../../models/right';
import { RightService } from '../../services/right.service';
import { GroupTrDropdownComponent } from '../group-tr-dropdown/group-tr-dropdown.component';

@Component({
  selector: 'cmdb-groups-list',
  templateUrl: './groups-list.component.html',
  styleUrls: ['./groups-list.component.scss']
})
export class GroupsListComponent implements OnInit, OnDestroy {

  public groupList: Group[];
  public rightList: Right[];

  @ViewChild(DataTableDirective, {static: false})
  private dtElement: DataTableDirective;
  private dtInstance: DataTables.Api;

  public dtOptions: DataTables.Settings = {};
  public dtTrigger: Subject<any> = new Subject();

  constructor(private groupService: GroupService, private rightService: RightService,
              private injector: Injector, private resolver: ComponentFactoryResolver, private app: ApplicationRef) {
  }

  public ngOnInit(): void {
    this.dtOptions = {
      ordering: false,
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
        this.dtElement.dtInstance.then((dtInstance: DataTables.Api) => {
          this.dtInstance = dtInstance;
        });
      }
    );

    this.rightService.getRightList().subscribe((rightList: Right[]) => {
      this.rightList = rightList;
    });
  }


  public toggle(group: Group) {
    const tr = document.getElementById(`tr_${group.name}`);
    const insertLabel = `tr_${group.public_id}`;
    const row = this.dtInstance.row(tr);
    if (row.child.isShown()) {
      document.getElementById(insertLabel).remove();
      row.child.hide();
      tr.classList.remove('shown');
    } else {
      row.child(`<div id="${insertLabel}"></div>`).show();
      const newTr = document.getElementById(insertLabel);
      const factory = this.resolver.resolveComponentFactory(GroupTrDropdownComponent);
      const ref = factory.create(this.injector, [], newTr);
      ref.instance.groupID = group.public_id;
      ref.instance.rightListNames = group.rights;
      ref.instance.completeRightList = this.rightList;
      this.app.attachView(ref.hostView);
      tr.classList.add('shown');
    }
  }

  public ngOnDestroy(): void {
    this.dtTrigger.unsubscribe();
  }

}
