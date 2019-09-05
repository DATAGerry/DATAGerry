import { Component, Input, OnInit } from '@angular/core';
import { LogMode } from '../../../../modes.enum';

@Component({
  selector: 'cmdb-object-log-change-view',
  templateUrl: './object-log-change-view.component.html',
  styleUrls: ['./object-log-change-view.component.scss']
})
export class ObjectLogChangeViewComponent {

  public modes = LogMode;
  @Input() action: LogMode;
  @Input() changes: any[];

  public constructor() {

  }

}
