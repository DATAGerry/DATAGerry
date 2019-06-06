import { Component, Input } from '@angular/core';

@Component({
  selector: 'cmdb-object-qr',
  templateUrl: './object-qr.component.html',
  styleUrls: ['./object-qr.component.scss']
})
export class ObjectQrComponent {
  public urlContent: string = null;

  constructor() {
    this.urlContent = window.location.href;
  }

}
