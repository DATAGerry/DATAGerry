import { Injectable } from '@angular/core';
import { ApiCallService, ApiService } from '../services/api-call.service';
import { CmdbStatus } from '../framework/models/cmdb-status';
import { map } from 'rxjs/operators';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ExportService<T = any> implements ApiService {

  public servicePrefix: string = 'export';

  constructor(private api: ApiCallService) {
  }

  public isTypeConfigValid(format: string, config: any): Observable<any> {
    /*
     Check if type config is valid
     */
    return this.api.callPost<any>(`${ this.servicePrefix }/type/${ format }/`, config).pipe(
      map((apiResponse) => {
        return apiResponse.body;
      })
    );
  }

  public queryTypeExport(format: string, config: any): Observable<any> {
    /*
     Get export file based on config
     */
    return this.api.callPost<any>(`${ this.servicePrefix }/type/${ format }/`, config).pipe(
      map((apiResponse) => {
        return apiResponse.body;
      })
    );
  }
}
