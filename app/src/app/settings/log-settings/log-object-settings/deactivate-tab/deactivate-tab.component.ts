import { Component, Input } from '@angular/core';
import { CmdbLog } from '../../../../framework/models/cmdb-log';

@Component({
  selector: 'cmdb-deactivate-tab',
  templateUrl: './deactivate-tab.component.html',
  styleUrls: ['./deactivate-tab.component.scss']
})
export class DeactivateTabComponent {

  @Input() public deletedLogList: CmdbLog[];

}
