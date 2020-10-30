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

/**
 * Order of sorting.
 */
export enum SortDirection {
  NONE = 0,
  ASCENDING = 1,
  DESCENDING = -1
}


/**
 * Interface for Sort/Order combination.
 */
export interface Sort {
  name: string;
  order: SortDirection;
}

/**
 * Interface for a table header.
 */
export interface Column {

  /**
   * Displayed name
   */
  display?: any;

  /**
   * Data value
   */
  data: any;

  /**
   * Identifier
   */
  name: string;

  /**
   * Field is hidden
   */
  hidden: boolean;

  /**
   * Field cant be toggled
   */
  fixed: boolean;

  /**
   * Sortable
   */
  sortable: boolean;

  /**
   * Searchable
   */
  searchable: boolean;

  /**
   * Got row template
   */
  template: TemplateRef<any>;

  /**
   * List of extra css classes for
   * head and cells in this column.
   */
  cssClasses: Array<string>;

  /**
   * Data parser
   * @param item
   * @param column
   * @param index
   */
  render(item?: any, column?: Column, index?: number);
}
