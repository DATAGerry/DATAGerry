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
import { UserSettingPayload } from '../../management/user-settings/models/user-setting';

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
  hidden?: boolean;

  /**
   * Field cant be toggled
   */
  fixed?: boolean;

  /**
   * Sortable
   */
  sortable?: boolean;

  /**
   * Searchable
   */
  searchable?: boolean;

  /**
   * Got row template
   */
  template?: TemplateRef<any>;

  /**
   * List of extra css classes for
   * head and cells in this column.
   */
  cssClasses?: Array<string>;

  /**
   * List of direct styles for
   * head and cells in this column.
   */
  style?: { [klass: string]: any };

  /**
   * Data parser
   * @param data
   * @param item
   * @param column
   * @param index
   */
  render(data: any, item: any, column?: Column, index?: number);
}

export interface TableConfig {
  columns: Array<Column>;
  page: number;
  pageSize: number;
  sort: Sort;
}

/**
 * Wrapper interface for a single table config inside the `ObjectTableUserSetting`.
 */
export interface TableConfigUserSetting {
  hash?: string;
  data: TableConfig;
  label: string;
  active: boolean;
}

/**
 * Represents a generic user setting for a specific config.
 * Will normally include into a `UserSetting` as payload.
 */
export class TableConfigPayload implements UserSettingPayload {
  public id: string;
  public tableConfigs: Array<TableConfigUserSetting>;

  public constructor(id: string, configs: Array<TableConfigUserSetting>) {
    this.id = id;
    this.tableConfigs = configs;
  }


}
