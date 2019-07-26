import { Component, Input } from '@angular/core';

@Component({
  selector: 'cmdb-object-actions',
  templateUrl: './object-actions.component.html',
  styleUrls: ['./object-actions.component.scss']
})
export class ObjectActionsComponent {

  @Input() objectID: number = 0;

}
