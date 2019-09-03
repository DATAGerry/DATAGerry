import { Component, Input } from '@angular/core';

@Component({
  selector: 'cmdb-object-footer',
  templateUrl: './object-footer.component.html',
  styleUrls: ['./object-footer.component.scss']
})
export class ObjectFooterComponent {

  @Input() publicID: number;

}
