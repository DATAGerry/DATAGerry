import { Component, EventEmitter, Input, Output } from '@angular/core';
import { TableColumnAction } from '../../../models/table-columns-action';

@Component({
  selector: 'cmdb-action-delete',
  templateUrl: './action-delete.component.html',
  styleUrls: ['./action-delete.component.scss']
})
export class ActionDeleteComponent {

  @Input() data: TableColumnAction[];
  @Input() publicID: string = '';
  @Output() deleteValue = new EventEmitter();

  delete(route: string) {
    this.deleteValue.emit(route);
  }
}
