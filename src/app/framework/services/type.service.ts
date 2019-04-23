import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { CmdbType } from '../models/cmdb-type';
import { ApiCallService } from '../../services/api-call.service';

@Injectable({
  providedIn: 'root'
})
export class TypeService {

  private servicePrefix: string = 'type/';

  constructor(private api: ApiCallService) {
  }

  public get listObservable(): Observable<CmdbType[]> {
    return this.api.callGetRoute<CmdbType[]>(this.servicePrefix);
  }
}
