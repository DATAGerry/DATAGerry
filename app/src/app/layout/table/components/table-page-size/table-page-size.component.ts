import { Component, Input, OnInit } from '@angular/core';


export interface PageLengthEntry {
  label: string | number;
  value: number;
}

@Component({
  // tslint:disable-next-line:component-selector
  selector: 'table-page-size',
  templateUrl: './table-page-size.component.html',
  styleUrls: ['./table-page-size.component.scss']
})
export class TablePageSizeComponent implements OnInit {

  @Input() public pageLength: number = 10;
  @Input() public pageLengthList: Array<PageLengthEntry> =
    [
      { label: '10', value: 10 },
      { label: '25', value: 10 },
      { label: '50', value: 10 },
      { label: '100', value: 10 },
      { label: '200', value: 10 },
      { label: '500', value: 10 },
      { label: 'All', value: 0 }
    ];

  constructor() {
  }

  ngOnInit() {
  }

}
