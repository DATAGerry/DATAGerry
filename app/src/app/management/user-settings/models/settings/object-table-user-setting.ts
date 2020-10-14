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

import { UserSettingPayload } from '../user-setting';

/**
 * Represents a generic user setting for a specific config.
 * Will normally include into a `UserSetting` as payload.
 */
export class ObjectTableUserPayload implements UserSettingPayload {
  public configs: Array<ObjectTableUserSettingConfig>;

  public constructor(configs: Array<ObjectTableUserSettingConfig>) {
    this.configs = configs;
  }
}

/**
 * Wrapper interface for a single table config inside the `ObjectTableUserSetting`.
 */
export interface ObjectTableUserSettingConfig {
  hash?: string;
  data: any;
  active: boolean;
}
