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

export class DataTableFilter {
  public start: number = 0;
  public length: number = 10;
  public orderBy: string = 'public_id';
  public direction: string = 'asc';
  public search: string = '';
}

export class DataTablesResult {
  public columns: any[];
  public data: any[];
  public recordsTotal: any;
  public recordsFiltered: any;
}

