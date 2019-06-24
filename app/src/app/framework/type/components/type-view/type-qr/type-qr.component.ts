import { Component, Input } from '@angular/core';

@Component({
  selector: 'cmdb-type-qr',
  templateUrl: './type-qr.component.html',
  styleUrls: ['./type-qr.component.scss']
})
export class TypeQrComponent {
  public urlContent: string = null;

  constructor() {
    this.urlContent = window.location.href;
  }

}
