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

import { Injectable } from '@angular/core';
import { isDevMode } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class ConnectionService {

  private readonly host: string;
  private readonly port: number;
  private readonly protocol: string;
  private readonly href: string;

  constructor() {
    if (isDevMode()) {
      this.host = '127.0.0.1';
      this.port = 4000; // fixed dev port
      this.protocol = 'http:';
    } else {
      this.host = window.location.hostname;
      this.port = +window.location.port;
      this.protocol = window.location.protocol;
    }
    this.href = `${this.protocol}//${this.host}:${this.port}/`;
  }

  public get connectionURL() {
    return this.href;
  }


}
