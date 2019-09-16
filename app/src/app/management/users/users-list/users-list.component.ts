import { Component, OnInit, ViewChild } from '@angular/core';
import { GroupService } from '../../services/group.service';
import { UserService } from '../../services/user.service';
import { DataTableDirective } from 'angular-datatables';
import { Subject } from 'rxjs';
import { User } from '../../models/user';
import { Group } from '../../models/group';

@Component({
  selector: 'cmdb-users-list',
  templateUrl: './users-list.component.html',
  styleUrls: ['./users-list.component.scss']
})
export class UsersListComponent implements OnInit {

  public userList: User[];

  @ViewChild(DataTableDirective, {static: false})
  private dtElement: DataTableDirective;

  public dtOptions: any = {};
  public dtTrigger: Subject<any> = new Subject();

  constructor(private userService: UserService, public groupService: GroupService) {
  }

  public ngOnInit(): void {
    this.dtOptions = {
      ordering: true,
      order: [[0, 'asc']],
      rowGroup: {
        endRender( rows, group ) {
          return `Number of users in this group: ${rows.count()}`;
        },
        dataSrc: 5
      },
      language: {
        search: '',
        searchPlaceholder: 'Filter...'
      }
    };

    this.userService.getUserList().subscribe((users: User[]) => {
        this.userList = users;
      },
      (error) => {
        console.error(error);
      }, () => {
        this.dtTrigger.next();
      }
    );
  }

}
