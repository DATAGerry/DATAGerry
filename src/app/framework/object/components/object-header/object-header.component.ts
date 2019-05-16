import { Component, Input } from '@angular/core';
import { CmdbType } from '../../../models/cmdb-type';

@Component({
  selector: 'cmdb-object-header',
  templateUrl: './object-header.component.html',
  styleUrls: ['./object-header.component.scss']
})
export class ObjectHeaderComponent {

  @Input() objectInstance: any = [];
  constructor() { }

}
