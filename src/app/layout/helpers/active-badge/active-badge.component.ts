import { Component, Input, OnInit } from '@angular/core';

@Component({
  selector: 'cmdb-active-badge',
  templateUrl: './active-badge.component.html',
  styleUrls: ['./active-badge.component.scss']
})
export class ActiveBadgeComponent implements OnInit {

  @Input() activeStatus: boolean;

  constructor() { }

  ngOnInit() {
  }

}
