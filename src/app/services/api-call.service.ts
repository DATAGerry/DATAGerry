import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders} from '@angular/common/http';
import {Observable} from 'rxjs';

const httpOptions = {
  headers: new HttpHeaders({
    'Content-Type': 'application/json'
  })
};

@Injectable({
  providedIn: 'root'
})
export class ApiCallService {

  hostAddress = 'localhost';
  hostPort = 4000;
  private readonly apiPrefix = 'rest';
  private readonly apiURL;

  constructor(private http: HttpClient) {
    this.apiURL = 'http://' + this.hostAddress + ':' + this.hostPort + '/' + this.apiPrefix + '/';
  }


  public callGetRoute<T>(route: string): Observable<any> {
    return this.http.get<T>(this.apiURL + route);
  }

  public async callAsyncGetRoute<T>(route: string): Promise<T> {
    return this.http.get<T>(this.apiURL + route).toPromise<T>();
  }

  public callPostRoute(route: string, data) {
    return this.http.post<any>(this.apiURL + route, data, httpOptions);
  }
}
