import { Component, Input } from '@angular/core';
import { CmdbType } from '../../../models/cmdb-type';

@Component({
  selector: 'cmdb-type-header',
  templateUrl: './type-header.component.html',
  styleUrls: ['./type-header.component.scss']
})
export class TypeHeaderComponent {

  @Input() typeInstance: CmdbType = null;
  constructor() { }

}
