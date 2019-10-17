import {Component, Input, OnInit} from '@angular/core';

@Component({
  selector: 'cmdb-import-type-complete',
  templateUrl: './import-type-complete.component.html',
  styleUrls: ['./import-type-complete.component.scss']
})
export class ImportTypeCompleteComponent implements OnInit {

  @Input() done: boolean;

  constructor() { }

  ngOnInit() {
  }
}
