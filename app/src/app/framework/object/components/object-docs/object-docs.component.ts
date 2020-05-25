import { Component, OnInit } from '@angular/core';

import { ObjectDocument } from '../../../models/cmdb-documents';
import { DocapiService } from '../../../../docapi/docapi.service';

@Component({
  selector: 'cmdb-object-docs',
  templateUrl: './object-docs.component.html',
  styleUrls: ['./object-docs.component.scss']
})
export class ObjectDocsComponent implements OnInit {

  docs: ObjectDocument[];

  constructor(private docapiService: DocapiService) { }

  ngOnInit() {
    this.docs = this.docapiService.getObjectDocumentsForType();
  }

}
