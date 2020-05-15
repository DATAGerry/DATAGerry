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


export class CmdbCategory implements CmdbDao {

  // tslint:disable: variable-name
  public public_id: number;
  public name: string;
  public label: string;
  public icon: string;
  public meta: {
    icon: string,
    order: number
  };
  public parent: any;
  // tslint:enable
}

export class CmdbCategoryNode{
  
}

export class CmdbCategoryTree {

  public category: CmdbCategory;

}

