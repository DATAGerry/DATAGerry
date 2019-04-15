import { Component, Input, OnInit } from '@angular/core';
import { ConnectionService } from './services/connection.service';
import { ConnectionResult } from './models/connection-result';

@Component({
  selector: 'cmdb-connection',
  templateUrl: './connection.component.html',
  styleUrls: ['./connection.component.scss']
})
export class ConnectionComponent implements OnInit {
  @Input() hostAddress = 'localhost';
  @Input() hostPort = 4000;
  public connectionResult: ConnectionResult;

  constructor(private connectionService: ConnectionService) {
  }

  public ngOnInit() {
    console.log('### Connection status ###');
    console.log(this.connectionService.currentConnection);
  }

  public onConnect() {
    this.connectionService.connect(this.hostAddress, this.hostPort).subscribe((result: ConnectionResult) => {
      this.connectionResult = result;
    });
  }

  public onDisconnect() {
    this.connectionService.disconnect();
  }

}
