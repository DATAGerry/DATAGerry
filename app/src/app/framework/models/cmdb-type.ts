/*
* DATAGERRY - OpenSource Enterprise CMDB
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

import { CmdbDao } from './cmdb-dao';


export class CmdbType implements CmdbDao {

  // tslint:disable:variable-name
  public readonly public_id: number;
  public name: string;
  public label?: string;
  public description?: string;
  public active: boolean;
  public author_id: number;
  public version: string;
  public creation_time: any;
  public render_meta: any;
  public fields: any[];
  public clean_db: boolean;

  public has_references(): boolean {
    for (const field of this.fields) {
      if (field.type === 'ref') {
        return true;
      }
    }
    return false;
  }

  public get_reference_fields() {
    const refFields = [];
    for (const field of this.fields) {
      if (field.type === 'ref') {
        refFields.push(field);
      }
    }
    return refFields;
  }

  // tslint:enable:variable-name
}
