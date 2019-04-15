import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse, HttpHeaders } from '@angular/common/http';
import { Connection } from '../models/connection';
import { ConnectionResult } from '../models/connection-result';
import { BehaviorSubject, Observable } from 'rxjs';
import { first } from 'rxjs/internal/operators/first';

const httpOptions = {
  headers: new HttpHeaders({
    'Content-Type': 'application/json',
  })
};

@Injectable({
  providedIn: 'root'
})
export class ConnectionService {

  private connectionSubject: BehaviorSubject<Connection>;
  public connection: Observable<Connection>;
  private connectionResultSubject: BehaviorSubject<ConnectionResult>;
  public connectionResult: Observable<ConnectionResult>;

  private readonly connectionSuffix: string = '/rest/';

  constructor(private http: HttpClient) {
    this.connectionSubject = new BehaviorSubject(JSON.parse(localStorage.getItem('connection')));
    this.connectionResultSubject = new BehaviorSubject(JSON.parse(localStorage.getItem('connection-result')));
    this.connection = this.connectionSubject.asObservable();
    this.connectionResult = this.connectionResultSubject.asObservable();
  }

  public connect(host: string, port: number) {
    const connectionBulk = this.http.get<ConnectionResult>(`http://${host}:${port}${this.connectionSuffix}`, httpOptions);
    connectionBulk.pipe(first()).subscribe(
      (connectionResult: ConnectionResult) => {
        connectionResult = connectionResult as ConnectionResult;
        const newConnection = new Connection(host, port);
        localStorage.setItem('connection', JSON.stringify(newConnection));
        this.connectionSubject.next(newConnection);
        localStorage.setItem('connection-result', JSON.stringify(connectionResult));
        this.connectionResultSubject.next(connectionResult);
        return connectionResult;
      },
      (error: HttpErrorResponse) => {
        this.disconnect();
      }
    );
    return connectionBulk;
  }

  public disconnect() {
    localStorage.removeItem('connection');
    this.connectionSubject.next(null);
    localStorage.removeItem('connection-result');
    this.connectionResultSubject.next(null);
  }

  public get currentConnection() {
    return this.connectionSubject.value;
  }

  public get currentConnectionResult() {
    return this.connectionResultSubject.value;
  }

  public get isConnected() {
    if (!this.currentConnection) {
      return false;
    } else if (!this.currentConnectionResult) {
      return false;
    } else {
      this.connect(this.currentConnection.host, this.currentConnection.port);
      return this.currentConnectionResult.connected;
    }
  }
}
