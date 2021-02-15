import {Component, Input} from '@angular/core';
import { RenderResult } from '../../../models/cmdb-render';

interface TypeRef {
  typeID: number;
  typeLabel: string;
  occurences: number;
}

@Component({
  selector: 'cmdb-object-references',
  templateUrl: './object-references.component.html',
  styleUrls: ['./object-references.component.scss']
})

export class ObjectReferencesComponent {

  @Input() publicID: number;

  referencedTypes: Array<TypeRef> = [];

  constructor() { }

  onReferencesLoaded(event: Array<RenderResult>) {
    this.referencedTypes = [];
    let objectList: Array<RenderResult> = Array.from(event);
    while (objectList.length > 0) {
      const typeID = objectList[0].type_information.type_id;
      const typeLabel = objectList[0].type_information.type_label;
      const occurences: number = objectList.filter(object => object.type_information.type_id === typeID).length;
      objectList = objectList.filter(object => object.type_information.type_id !== typeID);
      this.referencedTypes.push({typeID, typeLabel, occurences});
    }
  }

}
