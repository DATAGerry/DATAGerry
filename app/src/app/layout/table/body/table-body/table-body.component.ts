import { Component, Input, OnInit } from '@angular/core';
import { Column } from '../../models';

@Component({
  // tslint:disable-next-line:component-selector
  selector: 'tbody[table-body]',
  templateUrl: './table-body.component.html',
  styleUrls: ['./table-body.component.scss']
})
export class TableBodyComponent<T> implements OnInit {

  /**
   * Items which are displayed in the table.
   */
  @Input() public items: Array<T> = [];

  /**
   * Columns definition.
   */
  @Input() public columns: Array<Column> = [];

  constructor() { }

  ngOnInit() {
  }

}
