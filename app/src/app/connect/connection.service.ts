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

import { Injectable } from '@angular/core';
import { isDevMode } from '@angular/core';
import { HttpBackend, HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ConnectionService {

  private readonly devPort: number = 4000;  // fixed dev port

  private connectionSubject: BehaviorSubject<string>;
  public connection: Observable<string>;
  private connectionStatus: boolean = false;
  private http: HttpClient;

  public constructor(private backend: HttpBackend) {
    this.http = new HttpClient(backend);
    this.connectionSubject = new BehaviorSubject<string>(JSON.parse(localStorage.getItem('connection')));
    this.connection = this.connectionSubject.asObservable();

    if (this.currentConnection === null) {
      this.setDefaultConnection();
    }
    try {
      const connectionStatusPromise = this.connect();
      connectionStatusPromise.then(status => {
        this.connectionStatus = status;
        if (this.connectionStatus === false) {
          localStorage.removeItem('connection');
          this.connectionSubject.next(null);
        }
      });
    } catch (e) {
      this.connectionStatus = false;
      localStorage.removeItem('connection');
      this.connectionSubject.next(null);
    }


  }

  private setDefaultConnection() {
    if (isDevMode()) {
      this.setConnectionURL('http', '127.0.0.1', this.devPort);
    } else {
      this.setConnectionURL(
        window.location.protocol.substring(0, window.location.protocol.length - 1),
        window.location.hostname,
        +window.location.port
      );
    }
  }

  public get status(): boolean {
    return this.connectionStatus;
  }

  public get currentConnection(): any {
    return this.connectionSubject.value;
  }

  public async testConnection() {
    try {
      await this.connect();
      return true;
    } catch (e) {
      return false;
    }
  }

  private async connect() {
    console.log('######## CONNECTION TRY ########');
    console.log(`With URL: ${this.currentConnection}/rest/`);
    return await this.http.get<any>(`${this.currentConnection}/rest/`).toPromise();
  }

  public async testCustomURL(protocol: string, host: string, port: number) {
    const customURL = `${protocol}://${host}:${port}/rest/`;
    console.log(`Trying to connect to backend @ ${customURL}`);
    return await this.http.get<any>(customURL).toPromise();
  }

  public setConnectionURL(protocol: string, host: string, port: number) {
    let href = '';
    if (port === 0) {
      href = `${protocol}://${host}`;
    } else {
      href = `${protocol}://${host}:${port}`;
    }
    localStorage.setItem('connection', JSON.stringify(href));
    this.connectionSubject.next(href);
  }

}
