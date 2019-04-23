import { Component, Input } from '@angular/core';

@Component({
  selector: 'cmdb-content-header',
  templateUrl: './content-header.component.html',
  styleUrls: ['./content-header.component.scss']
})
export class ContentHeaderComponent {

  @Input() public title: string;

}
