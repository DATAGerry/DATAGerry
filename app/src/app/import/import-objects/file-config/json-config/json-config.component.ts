import { Component, OnInit } from '@angular/core';
import { FileConfig } from '../file-config';

@Component({
  selector: 'cmdb-json-config',
  templateUrl: './json-config.component.html',
  styleUrls: ['./json-config.component.scss']
})
export class JsonConfigComponent extends FileConfig implements OnInit {

  constructor() {
    super();
  }

  ngOnInit() {
  }

}
