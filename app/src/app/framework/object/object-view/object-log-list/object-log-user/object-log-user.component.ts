import { Component, Input, OnChanges, OnInit, SimpleChanges } from '@angular/core';
import { User } from '../../../../../management/models/user';
import { UserService } from '../../../../../management/services/user.service';

@Component({
  selector: 'cmdb-object-log-user',
  templateUrl: './object-log-user.component.html',
  styleUrls: ['./object-log-user.component.scss']
})
export class ObjectLogUserComponent implements OnChanges {

  @Input() userID: number = 0;
  @Input() userName: string = '';

  public logUser: User;
  public userExists: boolean = false;

  constructor(private userService: UserService) {
  }

  public ngOnChanges(changes: SimpleChanges): void {
    if (changes.userID !== undefined && changes.userID.isFirstChange()) {
      this.userService.getUser(this.userID).subscribe((possibleUser: User) => {
        this.logUser = possibleUser;
        this.userExists = true;
      }, () => {
        this.userExists = false;
      });
    }
  }


}
