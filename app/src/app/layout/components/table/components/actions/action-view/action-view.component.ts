import { Component, Input } from '@angular/core';
import { TableColumnAction } from '../../../models/table-columns-action';

@Component({
  selector: 'cmdb-action-view',
  templateUrl: './action-view.component.html',
  styleUrls: ['./action-view.component.scss']
})
export class ActionViewComponent {

  @Input() data: TableColumnAction[];
  @Input() publicID: string = '';
}
