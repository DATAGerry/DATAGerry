/*
* DATAGERRY - OpenSource Enterprise CMDB
* Copyright (C) 2024 becon GmbH
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


export class CmdbObject implements CmdbDao {

  public public_id: number;
  public type_id: number;
  public status: boolean = true;
  public version: string;
  public author_id: number;
  public editor_id?: number;
  public active: boolean;
  public fields: any[];
  public creation_time: any;
  public last_edit_time: any;
  public author_name?: string;
  public comment?: string;
}
