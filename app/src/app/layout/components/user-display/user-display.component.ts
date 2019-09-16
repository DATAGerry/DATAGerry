import { Component, Input, OnInit } from '@angular/core';
import { User } from '../../../management/models/user';

@Component({
  selector: 'cmdb-user-display',
  templateUrl: './user-display.component.html',
  styleUrls: ['./user-display.component.scss']
})
export class UserDisplayComponent {

  @Input() user: User;

  public get name() {
    if ((this.user.first_name !== null) && (this.user.last_name !== null)) {
      return `${this.user.first_name} ${this.user.last_name}`;
    }
    return this.user.user_name;
  }
}
