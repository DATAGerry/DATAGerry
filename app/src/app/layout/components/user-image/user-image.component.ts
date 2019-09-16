import { Component, Input, OnInit } from '@angular/core';

@Component({
  selector: 'cmdb-user-image',
  templateUrl: './user-image.component.html',
  styleUrls: ['./user-image.component.scss']
})
export class UserImageComponent {
  public defaultURL = '/assets/img/avatar.png';
  @Input() maxWidth: string = '200';
  @Input() imageURL: string;
}
