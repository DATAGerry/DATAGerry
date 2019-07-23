/*
* dataGerry - OpenSource Enterprise CMDB
* Copyright (C) 2019 NETHINKS GmbH
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
* along with this program.  If not, see <https://www.gnu.org/licenses/>.
*/

import { Component, Input } from '@angular/core';
import { CmdbObject } from '../../../models/cmdb-object';


class MetaView {
  private readonly headers: { [key: string]: object | string | number }[] = [
    {'Public ID': this.publicID},
    {'Creation Time': this.creationTime},
    {'Last Edit Time': this.lastEditTime},
    {'Author ID': this.authorID},
    {'Author Name': this.authorName}
  ];

  constructor(public publicID: number, public creationTime: object, public lastEditTime: object,
              public authorID: number, public authorName) {

  }

  public get headerLine() {
    return this.headers;
  }
}

@Component({
  selector: 'cmdb-object-view-meta',
  templateUrl: './object-view-meta.component.html',
  styleUrls: ['./object-view-meta.component.scss']
})
export class ObjectViewMetaComponent {

  public meteObject: MetaView = null;
  // tslint:disable-next-line:variable-name
  private _objectInstance: CmdbObject;
  @Input('objectInstance')
  public set objectInstance(data: CmdbObject) {
    if (data !== undefined) {
      this._objectInstance = data;
      this.meteObject = new MetaView(
        this.objectInstance.public_id, this.objectInstance.creation_time, this.objectInstance.last_edit_time,
        this.objectInstance.author_id, this.objectInstance.author_name
      );
    }

  }

  public get objectInstance(): CmdbObject {
    return this._objectInstance;
  }

  public isObject(value: object | string | number) {
    return typeof value === 'object';
  }


}




