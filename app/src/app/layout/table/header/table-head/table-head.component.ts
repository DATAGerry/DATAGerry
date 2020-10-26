import { Component, Input, OnInit } from '@angular/core';
import { Column } from '../../models';

@Component({
  // tslint:disable-next-line:component-selector
  selector: 'thead[table-head]',
  templateUrl: './table-head.component.html',
  styleUrls: ['./table-head.component.scss']
})
export class TableHeadComponent implements OnInit {

  /**
   * Columns definition.
   */
  @Input() public columns: Array<Column> = [];

  constructor() { }

  ngOnInit() {
  }

}
