import { Component, Input, OnInit } from '@angular/core';
import { RenderResult } from '../../../models/cmdb-render';
import { CollectionParameters } from '../../../../services/models/api-parameter';
import { APIGetMultiResponse } from '../../../../services/models/api-response';
import { ObjectService } from '../../../services/object.service';

interface TypeRef {
  typeID: number;
  typeLabel: string;
  typeName: string;
  occurences: number;
}

@Component({
  selector: 'cmdb-object-references',
  templateUrl: './object-references.component.html',
  styleUrls: ['./object-references.component.scss']
})

export class ObjectReferencesComponent implements OnInit {

  @Input() publicID: number;

  referencedTypes: Array<TypeRef> = [];

  constructor(public objectService: ObjectService) { }
  /**
   * Load/reload objects from the api.
   * @private
   */
  public ngOnInit() {

    const params: CollectionParameters = {
      filter: undefined,
      limit: 0,
      sort: 'public_id',
      order: 1,
      page: 1
    };

    const referenceSubscription = this.objectService.getObjectReferences(this.publicID, params).subscribe(
      (apiResponse: APIGetMultiResponse<RenderResult>) => {
        this.sortReferencesByType(apiResponse.results as Array<RenderResult>);
        referenceSubscription.unsubscribe();
      });
  }

  sortReferencesByType(event: Array<RenderResult>) {
    this.referencedTypes = [];
    let objectList: Array < RenderResult > = Array.from(event);
    while (objectList.length > 0) {
      const typeID = objectList[0].type_information.type_id;
      const typeLabel = objectList[0].type_information.type_label;
      const typeName = objectList[0].type_information.type_name;
      const occurences = objectList.filter(object => object.type_information.type_id === typeID);
      this.referencedTypes.push({typeID, typeLabel, typeName, occurences : occurences.length});
      objectList = objectList.filter(object => object.type_information.type_id !== typeID);
    }
    this.referencedTypes = this.referencedTypes.sort((a, b) => {
      if (a.occurences > b.occurences) {
        return -1;
      } else if (a.occurences < b.occurences) {
        return 1;
      } else {
        if (a.typeLabel > b.typeLabel) {
          return 1;
        } else if (a.typeLabel < b.typeLabel) {
          return -1;
        }
      }
      return 0;
    });
  }

}
