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

export class CmdbCollection implements CmdbDao {
  // tslint:disable: variable-name
  public public_id: number;
  public template_id: number;
  public creation_time: {
    $date: string;
  };
  public last_edit_time?: {
    $date: string;
  };
  public object_list: [];
  // tslint:enable
}

export class CmdbCollectionTemplate implements CmdbDao {
  // tslint:disable: variable-name
  public public_id: number;
  public name: string;
  public label?: string;
  public creation_time: {
    $date: string;
  };
  public last_edit_time?: {
    $date: string;
  };
  public type_order_list?: [];
  // tslint:enable
}
