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

import { CmdbDao } from '../../framework/models/cmdb-dao';

export class FileMetadata implements CmdbDao {

  // a set of data that describes and gives information about other data.
  // tslint:disable:variable-name
  public readonly public_id: number;
  public reference: number;
  public reference_type: string;
  public mime_type: string;
  public folder: boolean;
  public parent: number;
  public author_id: number;
  public permission: any;
  // tslint:enable:variable-name

  public constructor(init?: Partial<FileMetadata>) {
    Object.assign(this, init);
  }
}
