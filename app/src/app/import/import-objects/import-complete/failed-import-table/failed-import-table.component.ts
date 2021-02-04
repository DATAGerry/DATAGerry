import { Component, Input, OnInit, TemplateRef, ViewChild } from '@angular/core';
import { Column } from '../../../../layout/table/table.types';

@Component({
  selector: 'cmdb-failed-import-table',
  templateUrl: './failed-import-table.component.html',
  styleUrls: ['./failed-import-table.component.scss']
})
export class FailedImportTableComponent implements OnInit {

  @Input() failedImports: any = [];

  @ViewChild('errorTemplate', {static : true}) errorTemplate: TemplateRef<any>;

  @ViewChild('objectTemplate', {static : true}) objectTemplate: TemplateRef<any>;

  public columns: Column[] = [];

  constructor() { }

  ngOnInit() {
    this.columns = [
      {
        display: 'Error Message',
        name: 'error_message',
        data: 'error_message',
        template: this.errorTemplate
      },
      {
        display: 'Object',
        name: 'object',
        data: 'obj',
        template: this.objectTemplate
      }
    ] as Array<Column>;
  }

}
