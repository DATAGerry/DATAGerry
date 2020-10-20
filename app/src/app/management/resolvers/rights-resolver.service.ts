import { Injectable } from '@angular/core';
import { ActivatedRouteSnapshot, Resolve, RouterStateSnapshot } from '@angular/router';
import { Right } from '../models/right';
import { RightService } from '../services/right.service';
import { Observable } from 'rxjs';
import { APIGetMultiResponse } from '../../services/models/api-response';
import { map } from 'rxjs/operators';

/**
 * Resolver for the complete right list
 */
@Injectable({
  providedIn: 'root'
})
export class RightsResolver implements Resolve<Array<Right>> {

  constructor(private rightService: RightService) {
  }

  resolve(route: ActivatedRouteSnapshot, state: RouterStateSnapshot): Observable<Array<Right>> | Promise<Array<Right>> | Array<Right> {
    return this.rightService.getRights({ filter: undefined, limit: 0, sort: 'name', order: 1, page: 1 }).pipe(
      map((
        apiResponse: APIGetMultiResponse<Right>) => {
        return apiResponse.results as Array<Right>;
      }));
  }
}
