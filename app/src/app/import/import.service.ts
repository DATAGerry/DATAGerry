import { Injectable } from '@angular/core';
import { ApiCallService, ApiService, httpFileOptions, resp } from '../services/api-call.service';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { HttpHeaders, HttpParams } from '@angular/common/http';
import { ParserResponse } from './import-objects/preview/preview.model';

@Injectable({
  providedIn: 'root'
})
export class ImportService implements ApiService {

  public servicePrefix: string = 'import';
  private objectPrefix: string = 'object';

  constructor(private api: ApiCallService) {
  }

  public getObjectParserDefaultConfig(fileType: string): Observable<any> {
    return this.api.callGet<any>(`${ this.servicePrefix }/${ this.objectPrefix }/parser/default/${ fileType }/`).pipe(
      map((apiResponse) => {
        if (apiResponse.status === 204) {
          return {};
        }
        return apiResponse.body;
      })
    );
  }

  public postObjectParserFile(fileType: string, formData: FormData, config) {
    let httpParams = new HttpParams();
    Object.keys(config).forEach((key) => {
      httpParams = httpParams.append(key, config[key]);
    });

    const httpsdf = httpFileOptions;
    httpsdf.params = httpParams
    return this.api.callPost<ParserResponse>(
      `${ this.servicePrefix }/${ this.objectPrefix }/parser/${ fileType }/`, formData, httpsdf).pipe(
      map((apiResponse) => {
        return apiResponse.body;
      })
    );
  }

  public getObjectImporters(): Observable<string[]> {
    return this.api.callGet<string[]>(`${ this.servicePrefix }/${ this.objectPrefix }/importer/`).pipe(
      map((apiResponse) => {
        if (apiResponse.status === 204) {
          return [];
        }
        return apiResponse.body;
      })
    );
  }

}
