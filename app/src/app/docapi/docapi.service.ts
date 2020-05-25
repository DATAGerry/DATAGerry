import { Injectable } from '@angular/core';

import { ObjectDocument } from '../framework/models/cmdb-documents';

@Injectable({
  providedIn: 'root'
})
export class DocapiService {

  constructor() { }

  getObjectDocumentsForType() : ObjectDocument[] {
    let docs: ObjectDocument[] = [
      {id: 1, name: 'label', label: 'Label'},
      {id: 2, name: 'contract', label: 'Support Contract'}
    ];
    return docs;
  }
}
