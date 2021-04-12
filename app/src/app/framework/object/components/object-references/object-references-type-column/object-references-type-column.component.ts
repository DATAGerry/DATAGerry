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

import { Component, Input } from '@angular/core';
import { CmdbObject } from '../../../../models/cmdb-object';
import { RenderResult } from '../../../../models/cmdb-render';

@Component({
  selector: 'cmdb-object-references-type-column',
  templateUrl: './object-references-type-column.component.html',
  styleUrls: ['./object-references-type-column.component.scss']
})
export class ObjectReferencesTypeColumnComponent {

  public isSectionRef: boolean = false;
  public isFieldRef: boolean = false;

  /**
   * ID of the referenced object.
   */
  @Input() public objectID: number;

  /**
   * Reference object
   */
  public renderResult: CmdbObject | RenderResult;

  /**
   * Reference object setter
   */
  @Input('object')
  public set Object(obj: CmdbObject | RenderResult) {
    if (obj) {
      this.renderResult = obj;
      this.isSectionRef = this.refTypeIsInFields(obj.fields, 'ref-section-field');
      this.isFieldRef = this.refTypeIsInFields(obj.fields, 'ref');
    }

  }

  /**
   * Check if a ref type is in fields
   * @param fields
   * @param type
   * @private
   */
  private refTypeIsInFields(fields: Array<any>, type: string): boolean {
    return fields.find(f => f.type === type && f.value === this.objectID) !== undefined;
  }


}
