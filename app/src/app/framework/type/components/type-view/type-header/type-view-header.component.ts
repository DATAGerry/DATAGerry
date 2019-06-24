import { Component, Input } from '@angular/core';
import { CmdbType } from '../../../../models/cmdb-type';

@Component({
  selector: 'cmdb-type-view-header',
  templateUrl: './type-view-header.component.html',
  styleUrls: ['./type-view-header.component.scss']
})
export class TypeViewHeaderComponent {

  @Input() typeInstance: CmdbType = null;
  constructor() { }

}
