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

import { Component, Input, OnInit } from '@angular/core';
import { ConnectionService } from './services/connection.service';
import { ConnectionResult } from './models/connection-result';
import { Router } from '@angular/router';

@Component({
  selector: 'cmdb-connection',
  templateUrl: './connection.component.html',
  styleUrls: ['./connection.component.scss']
})
export class ConnectionComponent implements OnInit {
  @Input() hostAddress = 'localhost';
  @Input() hostPort = 4000;
  public connectionResult: ConnectionResult;

  constructor(private connectionService: ConnectionService, private route: Router) {
  }

  public ngOnInit() {
    console.log('### Connection status ###');
    console.log(this.connectionService.currentConnection);
  }

  public onConnect() {
    this.connectionService.connect(this.hostAddress, this.hostPort).subscribe((result: ConnectionResult) => {
      this.connectionResult = result;
      if (this.connectionService.isConnected) {
        this.route.navigate(['/']);
      }
    });
  }

  public onDisconnect() {
    this.connectionService.disconnect();
  }

}
