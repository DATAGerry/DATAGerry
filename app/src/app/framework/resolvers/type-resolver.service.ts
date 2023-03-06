/*
* DATAGERRY - OpenSource Enterprise CMDB
* Copyright (C) 2023 becon GmbH
*
* This program is free software: you can redistribute it and/or modify
* it under the terms of the GNU Affero General Public License as
* published by the Free Software Foundation, either version 3 of the
* License, or (at your option) any later version.
*
* This program is distributed in the hope that it will be useful,
* but WITHOUT ANY WARRANTY; without even the implied warranty of
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
* GNU Affero General Public License for more details.

* You should have received a copy of the GNU Affero General Public License
* along with this program. If not, see <https://www.gnu.org/licenses/>.
*/

import { Injectable } from '@angular/core';
import { CmdbType } from '../models/cmdb-type';
import { ActivatedRouteSnapshot, Resolve, RouterStateSnapshot } from '@angular/router';
import { Observable } from 'rxjs';
import { TypeService } from '../services/type.service';

/**
 * Service class for resolving a typeID to a `CmdbType`.
 */
@Injectable({
  providedIn: 'root'
})
export class TypeResolver implements Resolve<CmdbType> {

  constructor(private typeService: TypeService) {
  }

  /**
   * Resolves the passed TypeID to a `CmdbType`.
   * @param route ActivatedRouteSnapshot
   * @param state RouterStateSnapshot
   */
  public resolve(route: ActivatedRouteSnapshot, state: RouterStateSnapshot):
    Observable<CmdbType> | Promise<CmdbType> | CmdbType {
    const typeID: number = +route.paramMap.get('typeID');
    return this.typeService.getType(typeID);
  }
}
