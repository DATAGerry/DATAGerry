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
* along with this program. If not, see <https://www.gnu.org/licenses/>.
*/

import { TemplateRef } from '@angular/core';

export class Pagination {

}


/**
 * Interface for Sort/Order combination.
 */
export interface Sort {
  name: string;
  order: number;
}

/**
 * Interface for a table header.
 */
export interface Column {
  display: any;
  data: any;
  name: string;
  hidden: boolean;
  fixed: boolean;
  sortable: boolean;

  render(item?: any, column?: Column, index?: number, container?: TemplateRef<any>);
}

export class TableConfig<T> {
  pageLength: number = 10;
  currentPage: number = 1;
  items: Array<T> = [];
  totalItems: number = this.items.length;
}
