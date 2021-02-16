/*
* DATAGERRY - OpenSource Enterprise CMDB
* Copyright (C) 2019 - 2021 NETHINKS GmbH
*
* This program is free software: you can redistribute it and/or modify
* it under the terms of the GNU Affero General Public License as
* published by the Free Software Foundation, either version 3 of the
* License, or (at your option) any later version.
*
* This program is distributed in the hope that it will be useful,
* but WITHOUT ANY WARRANTY; without even the implied warranty of
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
* GNU Affero General Public License for more details.

* You should have received a copy of the GNU Affero General Public License
* along with this program. If not, see <https://www.gnu.org/licenses/>.
*/

import { Component, Input, OnInit } from '@angular/core';
import { RenderResult } from '../../../models/cmdb-render';
import { CollectionParameters } from '../../../../services/models/api-parameter';
import { APIGetMultiResponse } from '../../../../services/models/api-response';
import { ObjectService } from '../../../services/object.service';
import { Subject } from 'rxjs';

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

  clickSubject: Subject<string> = new Subject<string>();

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

  onClick(event) {
    this.clickSubject.next(event);
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
