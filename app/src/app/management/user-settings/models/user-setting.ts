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

import { ObjectStoreSchema } from 'ngx-indexed-db/lib/ngx-indexed-db.meta';

export const userSettingsSchema: ObjectStoreSchema[] = [
  { name: 'id', keypath: 'id', options: { unique: true } },
  { name: 'user_id', keypath: 'user_id', options: { unique: false } },
  { name: 'payloads', keypath: 'payloads', options: { unique: false } },
  { name: 'setting_type', keypath: 'setting_type', options: { unique: false } }
];

/**
 * Basic user setting class. Wrapper class for all CRUD functions with the API.
 */
export class UserSetting<P = UserSettingPayload> {
  id: string;
  user_id: number;
  payloads: Array<P>;
  setting_type: string;

  constructor(id: string, user_id: number, payloads: Array<P>) {
    this.id = id;
    this.user_id = user_id;
    this.payloads = payloads;
    this.setting_type = 'APPLICATION';
  }
}

// tslint:disable-next-line:no-empty-interface
export interface UserSettingPayload {
  id: string;
}
