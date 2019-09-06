import { Component, Input, OnInit } from '@angular/core';
import { CmdbLog } from '../../../../framework/models/cmdb-log';

@Component({
  selector: 'cmdb-activate-tab',
  templateUrl: './activate-tab.component.html',
  styleUrls: ['./activate-tab.component.scss']
})
export class ActivateTabComponent {

  @Input() public activeLogList: CmdbLog[];

}
