import { Injectable } from '@angular/core';
import { ActivatedRouteSnapshot, Resolve, RouterStateSnapshot } from '@angular/router';
import { Right } from '../models/right';
import { RightService } from '../services/right.service';
import { Observable } from 'rxjs';

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
    return undefined;
  }
}
