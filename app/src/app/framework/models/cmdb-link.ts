/*
* DATAGERRY - OpenSource Enterprise CMDB
* Copyright (C) 2023 becon GmbH
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
import { RenderResult } from './cmdb-render';

export class CmdbLink implements CmdbDao {

  // tslint:disable:variable-name
  public readonly public_id: number;
  public primary: number;
  public secondary: number;
  public creation_time: Date;
  public partnerObject?: RenderResult;
  // tslint:enable:variable-name
}
