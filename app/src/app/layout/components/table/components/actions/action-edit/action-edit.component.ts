import {Component, Input, OnInit} from '@angular/core';
import {TableColumnAction} from '../../../models/table-columns-action';

@Component({
  selector: 'cmdb-action-edit',
  templateUrl: './action-edit.component.html',
  styleUrls: ['./action-edit.component.scss']
})
export class ActionEditComponent implements OnInit {

  @Input() data: TableColumnAction[];
  @Input() publicID: string = '';

  constructor() { }

  ngOnInit() {
  }

}
