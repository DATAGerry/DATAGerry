import { Injectable } from '@angular/core';
import { ApiCallService } from '../../services/api-call.service';

@Injectable({
  providedIn: 'root'
})
export class ObjectService {

  private servicePrefix: string = 'object';
  constructor(private api: ApiCallService) { }
}
