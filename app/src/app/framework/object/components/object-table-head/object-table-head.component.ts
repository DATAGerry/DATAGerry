import {Component, EventEmitter, Input, OnChanges, OnDestroy, OnInit, Output} from '@angular/core';
import {CmdbType} from '../../../models/cmdb-type';
import {Router} from '@angular/router';

@Component({
  selector: 'cmdb-object-table-head',
  templateUrl: './object-table-head.component.html',
  styleUrls: ['./object-table-head.component.scss']
})
export class ObjectTableHeadComponent {

  private objectType: CmdbType;
  @Input() set type(type: CmdbType) {
    this.objectType = type;
  }
  get type(): CmdbType {
    return this.objectType;
  }

  @Input() selectedObjects: Array<number> = [];
  @Input() formatList: any[] = [];
  @Input() totalResults: number = 0;

  @Output() fileExport: EventEmitter<any> = new EventEmitter<any>();
  @Output() manyObjectDeletes: EventEmitter<any> = new EventEmitter<any>();


}
