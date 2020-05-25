import { Component, OnInit } from '@angular/core';

import { ObjectDocument } from '../../../models/cmdb-documents';

@Component({
  selector: 'cmdb-object-docs',
  templateUrl: './object-docs.component.html',
  styleUrls: ['./object-docs.component.scss']
})
export class ObjectDocsComponent implements OnInit {

  docs: ObjectDocument[] = [
    {id: 1, name: 'label', label: 'Label'},
    {id: 2, name: 'contract', label: 'Support Contract'}
  ];

  constructor() { }

  ngOnInit() {
  }

}
