import { Injectable } from '@angular/core';
import { ApiCallService, ApiService } from '../../services/api-call.service';
import { Observable } from 'rxjs';
import { CmdbStatus } from '../../framework/models/cmdb-status';
import { map } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class SystemService<T = any> implements ApiService  {

  public servicePrefix: string = 'settings/system';
  constructor(private api: ApiCallService) { }

  public getDatagerryInformation(): Observable<T> {
    return this.api.callGet<T>(`${this.servicePrefix}/`).pipe(
      map((apiResponse) => {
        return apiResponse.body;
      })
    );
  }

  public getConfigInformation(): Observable<T> {
    return this.api.callGet<T>(`${this.servicePrefix}/config/`).pipe(
      map((apiResponse) => {
        return apiResponse.body;
      })
    );
  }

  public reloadConfigFile(): Observable<T> {
    return this.api.callPost<T>(`${this.servicePrefix}/config/`, true).pipe(
      map((apiResponse) => {
        return apiResponse.body;
      })
    );
  }


}
