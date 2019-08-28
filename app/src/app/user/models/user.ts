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

export class User {
  /* tslint:disable */
  readonly public_id: number;
  public user_name: string;
  public first_name?: string;
  public last_name?: string;
  public email: string;
  public token?: string;
  public token_expire?: number;
  public registration_time: any;
  public authenticator: string;
  public group_id: number;

  public getName() {
    if (typeof this.first_name != 'undefined' || typeof this.last_name != 'undefined') {
      return this.user_name;
    }
    return this.first_name + ' ' + this.last_name;
  }
  /* tslint:enable */
}
