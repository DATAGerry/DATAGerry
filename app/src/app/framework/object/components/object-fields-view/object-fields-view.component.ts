import {Component, Input } from '@angular/core';

@Component({
  selector: 'cmdb-object-fields-view',
  templateUrl: './object-fields-view.component.html',
  styleUrls: ['./object-fields-view.component.scss']
})
export class ObjectFieldsViewComponent {

  @Input() objectInstance: any = [];
  constructor() { }

}
