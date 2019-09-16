import { Component, Input, OnChanges, OnInit, SimpleChanges } from '@angular/core';
import { Right } from '../../models/right';
import { UserService } from '../../services/user.service';
import { User } from '../../models/user';

@Component({
  selector: 'cmdb-group-rights-list',
  templateUrl: './group-tr-dropdown.component.html',
  styleUrls: ['./group-tr-dropdown.component.scss']
})
export class GroupTrDropdownComponent implements OnInit, OnChanges {

  @Input() groupID: number;
  @Input() rightListNames: string[];
  @Input() completeRightList: Right[];
  public rightList: Right[] = [];
  public groupUsers: User[] = [];

  public constructor(private userService: UserService) {

  }

  public ngOnInit(): void {
    this.userService.getUserByGroup(this.groupID).subscribe((users: User[]) => {
      this.groupUsers = users;
    });
  }

  public ngOnChanges(changes: SimpleChanges): void {
  }

  private loadRightList() {
    this.rightList = [];
    for (const rightName in this.rightListNames) {
      console.log(rightName);
    }
  }

}
